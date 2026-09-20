import hashlib
import os
import tempfile
from pathlib import Path

import streamlit as st

from src.auth_ui import logout_button, require_login
from src.explainer import explain
from src.pdf_report import _range as range_text
from src.pdf_report import build_pdf
from src.pipeline import analyze
from src.qa import answer_question
from src.store import get_history, init_reports_table, list_tracked_tests, save_report
from src.trends import analyze_trend
from src.ui_style import chat_bubble, dot, hero, inject, key_point_card, urgency_banner
from src.voice import build_spoken_script, speak, transcribe

st.set_page_config(page_title="ReportSathi", page_icon="🩺", layout="centered")
inject()

if not require_login():
    st.stop()

init_reports_table()
user = st.session_state["user"]
logout_button()

hero()

col1, col2 = st.columns([2, 1])
with col1:
    uploaded = st.file_uploader(
        "📄 Upload a report (PDF or photo)",
        type=["pdf", "png", "jpg", "jpeg", "webp"],
    )
with col2:
    language = st.selectbox("🌐 Explain in", ["English", "Hindi", "Bengali"])

go = st.button("✨ Explain my report", type="primary", use_container_width=True, disabled=not uploaded)

if go:
    suffix = Path(uploaded.name).suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded.getvalue())
    tmp.close()
    try:
        with st.status("Reading your report...", expanded=False) as status:
            result = analyze(tmp.name)
            status.update(label=f"Writing the explanation in {language}...")
            explained = explain(result, language)
            status.update(label="Done", state="complete")

        save_report(user["id"], result)

        pdf_bytes = None
        if language == "English":
            pdf_path = os.path.join(tempfile.gettempdir(), "reportsathi_summary.pdf")
            build_pdf(result, explained, pdf_path)
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            os.remove(pdf_path)

        st.session_state["output"] = {
            "result": result, "explained": explained,
            "pdf": pdf_bytes, "language": language, "qa": [],
        }
        st.toast("Saved to your health timeline.", icon="📈")
    except Exception as e:
        st.session_state.pop("output", None)
        st.error("Something went wrong while reading this report. Please try again.")
        with st.expander("Technical details"):
            st.code(str(e))
    finally:
        os.remove(tmp.name)

out = st.session_state.get("output")

tab_names = ["📋 Summary", "🔍 Values & Findings", "💬 Ask a question", "📈 Health Timeline", "🩺 Doctor visit"]
tab_summary, tab_values, tab_ask, tab_timeline, tab_doctor = st.tabs(tab_names)

# Small icon per body part / finding, purely to give the findings list a bit
# more visual variety — falls back to a generic icon when nothing matches.
_BODY_ICONS = {
    "liver": "🫀", "kidney": "🫘", "heart": "❤️", "lung": "🫁", "chest": "🫁",
    "brain": "🧠", "abdomen": "🩻", "spine": "🦴", "bone": "🦴", "thyroid": "🦋",
    "uterus": "🌸", "ovary": "🌸", "pancreas": "🫀", "gallbladder": "🫘",
    "spleen": "🩻", "stomach": "🩻", "bladder": "🩻", "prostate": "🩻",
}


def _icon_for(text: str) -> str:
    low = (text or "").lower()
    for key, icon in _BODY_ICONS.items():
        if key in low:
            return icon
    return "🔎"


if out:
    result, explained = out["result"], out["explained"]
    e = explained.explanation
    out.setdefault("qa", [])

    with tab_summary:
        urgency_banner(explained.urgency, explained.urgency_reason)
        st.write(e.summary)
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("🔊 Listen"):
                try:
                    with st.spinner("Creating audio..."):
                        out["audio"] = speak(build_spoken_script(explained, out["language"]), out["language"])
                except Exception as ex:
                    st.error("Could not create the audio.")
                    with st.expander("Technical details"):
                        st.code(str(ex))
        if out.get("audio"):
            st.audio(out["audio"], format="audio/wav")

        if e.connect_the_dots:
            st.markdown("##### 🧩 Patterns worth discussing")
            for d in e.connect_the_dots:
                dot(d)

    with tab_values:
        attention = [c for c in result.checked_values if c.status in ("low", "high")]
        normal = [c for c in result.checked_values if c.status == "normal"]
        key_by_name = {k.name: k for k in e.key_points}

        if attention:
            st.markdown("##### ⚠️ Lab values needing attention")
            for c in attention:
                kp = key_by_name.get(c.name)
                meaning = kp.meaning if kp else f"{c.value_text} {c.unit or ''} · printed range {range_text(c)}"
                key_point_card(c.name, c.status, meaning, c.deviation_pct)

        if normal:
            if attention:
                st.divider()
            st.markdown("##### ✅ Values within the normal range")
            for c in normal:
                kp = key_by_name.get(c.name)
                meaning = kp.meaning if kp else f"{c.value_text} {c.unit or ''} · printed range {range_text(c)}"
                key_point_card(c.name, c.status, meaning)

        if result.narrative:
            if attention or normal:
                st.divider()
            st.markdown(f"##### {_icon_for(result.narrative.modality)} {result.narrative.modality}")
            for f in result.narrative.findings:
                kp = key_by_name.get(f.body_part or f.finding[:30])
                meaning = kp.meaning if kp else f.finding
                label = f"{_icon_for(f.body_part)} {f.body_part}" if f.body_part else "Finding"
                key_point_card(label, f.significance, meaning)

            with st.expander("📜 Original wording from the report"):
                for f in result.narrative.findings:
                    st.write(f"- **{f.body_part or 'Finding'}:** {f.finding}")
                if result.narrative.impression:
                    st.write("**Impression:** " + result.narrative.impression)

        if not attention and not normal and not result.narrative:
            st.success("No values or findings were found in this report.")

    with tab_ask:
        st.caption("💡 Answers use only the facts from this report.")

        for item in out["qa"]:
            chat_bubble("user", item["q"])
            chat_bubble("ai", item["a"])
            if item.get("audio"):
                st.audio(item["audio"], format="audio/wav")

        def handle_question(question):
            try:
                with st.spinner("Thinking..."):
                    answer = answer_question(question, result, out["language"])
            except Exception as ex:
                st.error("Could not answer right now. Please try again.")
                with st.expander("Technical details"):
                    st.code(str(ex))
                return
            audio = None
            try:
                audio = speak(answer[:2400], out["language"])
            except Exception:
                pass
            out["qa"].append({"q": question, "a": answer, "audio": audio})
            st.rerun()

        with st.form("ask_form", clear_on_submit=True):
            typed = st.text_input("Type your question", placeholder="e.g. Is this serious?")
            asked = st.form_submit_button("Ask", use_container_width=True)
        if asked and typed.strip():
            handle_question(typed.strip())

        voice = st.audio_input("🎙️ Or ask by voice")
        if voice is not None:
            data = voice.getvalue()
            key = hashlib.md5(data).hexdigest()
            if out.get("last_voice") != key:
                out["last_voice"] = key
                try:
                    with st.spinner("Listening..."):
                        heard = transcribe(data, out["language"])
                except Exception as ex:
                    heard = ""
                    st.error("Could not understand the audio. Please try again.")
                    with st.expander("Technical details"):
                        st.code(str(ex))
                if heard.strip():
                    handle_question(heard.strip())

        if not out["qa"]:
            st.markdown("###### Or try one of these")
            for q in e.questions_for_doctor[:3]:
                if st.button(f"💬 {q}", key=f"suggest-{q}", use_container_width=True):
                    handle_question(q)

    with tab_doctor:
        st.markdown("##### ❓ Questions to ask your doctor")
        for q in e.questions_for_doctor:
            dot(q)
        st.markdown("")
        if out["pdf"]:
            st.download_button("⬇️ Download doctor summary (PDF)", out["pdf"],
                               file_name="reportsathi_summary.pdf", mime="application/pdf",
                               use_container_width=True)
        else:
            st.caption("The PDF summary is available in English for now. Choose English to download it.")
        st.caption(explained.disclaimer)
else:
    with tab_summary:
        st.info("⬆️ Upload a report above to see your explanation here.")
    with tab_values:
        st.info("⬆️ Upload a report above to see your values and findings here.")
    with tab_ask:
        st.info("⬆️ Upload a report above, then come back here to ask questions about it.")
    with tab_doctor:
        st.info("⬆️ Upload a report above to get your doctor-visit summary here.")

with tab_timeline:
    st.markdown("##### 📈 Your health timeline")
    tests = list_tracked_tests(user["id"])
    if not tests:
        st.info("Upload a report to start building your timeline. Once you have 2 or more reports "
                "with the same test, you'll see trends here.")
    else:
        picked = st.selectbox("Pick a test to track", tests)
        history = get_history(user["id"], picked)

        if len(history) < 2:
            st.warning(f"Only 1 report has {picked} so far. Upload another report with this test "
                      "to see a trend.")
        else:
            trend = analyze_trend(history, picked)

            chart_data = {"Report #": list(range(1, len(history) + 1)),
                         picked: [h["value"] for h in history]}
            st.line_chart(chart_data, x="Report #", y=picked)

            if trend.watch:
                st.warning(f"⚠️ **Worth watching:** {trend.message}", icon="⚠️")
            elif trend.direction == "stable":
                st.success(f"✅ {trend.message}")
            else:
                st.info(f"ℹ️ {trend.message}")

            st.caption(
                f"Direction: **{trend.direction}** · Latest status: **{trend.latest_status}** · "
                f"Based on {len(history)} saved reports."
            )