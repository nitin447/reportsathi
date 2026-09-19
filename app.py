import hashlib
import os
import tempfile
from pathlib import Path

import streamlit as st

from src.explainer import explain
from src.pdf_report import _range as range_text
from src.pdf_report import build_pdf
from src.pipeline import analyze
from src.qa import answer_question
from src.voice import build_spoken_script, speak, transcribe

st.set_page_config(page_title="ReportSathi", page_icon="🩺", layout="centered")

st.title("ReportSathi")
st.caption("Understand your medical reports, in your language.")
st.warning(
    "Development mode: upload only sample or fake reports. Free-tier AI services "
    "may use uploaded content to improve their products."
)

language = st.selectbox("Explain in", ["English", "Hindi", "Bengali"])
uploaded = st.file_uploader("Upload a report (PDF or photo)",
                            type=["pdf", "png", "jpg", "jpeg", "webp"])

if uploaded and st.button("Explain my report", type="primary"):
    suffix = Path(uploaded.name).suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded.getvalue())
    tmp.close()
    try:
        with st.spinner("Reading your report..."):
            result = analyze(tmp.name)
        with st.spinner(f"Writing the explanation in {language}..."):
            explained = explain(result, language)

        pdf_bytes = None
        if language == "English":
            pdf_path = os.path.join(tempfile.gettempdir(), "reportsathi_summary.pdf")
            build_pdf(result, explained, pdf_path)
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            os.remove(pdf_path)

        st.session_state["output"] = {
            "result": result, "explained": explained,
            "pdf": pdf_bytes, "language": language,
        }
    except Exception as e:
        st.session_state.pop("output", None)
        st.error("Something went wrong while reading this report. Please try again.")
        with st.expander("Technical details"):
            st.code(str(e))
    finally:
        os.remove(tmp.name)

out = st.session_state.get("output")
if out:
    result, explained = out["result"], out["explained"]
    e = explained.explanation

    st.divider()
    banner = {
        "urgent": st.error,
        "see_doctor_soon": st.warning,
        "routine_followup": st.info,
        "all_normal": st.success,
    }[explained.urgency]
    banner(explained.urgency_reason)

    st.subheader("Summary")
    st.write(e.summary)

    if st.button("Listen to this explanation"):
        try:
            with st.spinner("Creating audio..."):
                out["audio"] = speak(build_spoken_script(explained, out["language"]), out["language"])
        except Exception as ex:
            st.error("Could not create the audio. Check your Sarvam key and try again.")
            with st.expander("Technical details"):
                st.code(str(ex))
    if out.get("audio"):
        st.audio(out["audio"], format="audio/wav")

    attention = [c for c in result.checked_values if c.status in ("low", "high")]
    if attention:
        st.subheader("Values needing attention")
        st.dataframe(
            [{
                "Test": c.name,
                "Result": f"{c.value_text} {c.unit or ''}".strip(),
                "Printed range": range_text(c),
                "Status": c.status.upper() + (f" ({c.severity})" if c.severity else ""),
            } for c in attention],
            hide_index=True, width="stretch",
        )

    if result.narrative:
        with st.expander(f"{result.narrative.modality}: what the report says (original wording)"):
            for f in result.narrative.findings:
                if f.significance in ("abnormal", "borderline"):
                    st.write(f"- **{f.body_part or 'Finding'}:** {f.finding}")
            if result.narrative.impression:
                st.write("**Impression:** " + result.narrative.impression)

    if e.key_points:
        st.subheader("What this means")
        for k in e.key_points:
            st.markdown(f"**{k.name}** ({k.status}): {k.meaning}")

    if e.connect_the_dots:
        st.subheader("Patterns worth discussing")
        for d in e.connect_the_dots:
            st.write(f"- {d}")

    st.subheader("Questions to ask your doctor")
    for q in e.questions_for_doctor:
        st.write(f"- {q}")

    st.divider()
    st.subheader("Ask a question about this report")
    out.setdefault("qa", [])

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
            pass  # the text answer still shows
        out["qa"].append({"q": question, "a": answer, "audio": audio})

    with st.form("ask_form", clear_on_submit=True):
        typed = st.text_input("Type your question")
        asked = st.form_submit_button("Ask")
    if asked and typed.strip():
        handle_question(typed.strip())

    voice = st.audio_input("Or ask by voice")
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

    for item in reversed(out["qa"]):
        st.markdown(f"**You:** {item['q']}")
        st.write(item["a"])
        if item["audio"]:
            st.audio(item["audio"], format="audio/wav")

    st.divider()
    if out["pdf"]:
        st.download_button("Download doctor summary (PDF)", out["pdf"],
                           file_name="reportsathi_summary.pdf", mime="application/pdf")
    else:
        st.caption("The PDF summary is available in English for now. Choose English to download it.")

    st.caption(explained.disclaimer)