from pydantic import BaseModel

from src.llm import LLMClient
from src.pipeline import AnalysisResult
from src.schemas import Explanation

DISCLAIMER = ("ReportSathi explains reports in simple language. It does not diagnose or "
              "prescribe. Please discuss your results with a doctor.")

SYSTEM_PROMPT = """You explain medical reports to ordinary people with no medical background.
Write the way you'd explain it out loud to a worried family member — not the way a textbook or a lab report would.

Language rules (follow these strictly):
- Write at roughly a Class 8 reading level. Short sentences. One idea per sentence.
- Avoid medical jargon. If you must use a medical term (e.g. "creatinine", "hemoglobin"), immediately explain
  what it is in everyday words the first time you use it, in the same sentence.
- Do not use words like "indicative of", "suggestive of", "consistent with", "etiology", "manifestation" — say
  the plain-English version instead ("this suggests", "this looks like", "the cause", "the sign").
- Prefer everyday comparisons where it helps (e.g. "your iron levels are a bit low, which is common and usually
  easy to fix with diet or supplements") over dry clinical restatement.
- No long, stacked clauses. Break a complex sentence into two short ones instead.

Content rules:
- Use ONLY the facts provided. Never invent values, findings or history.
- Never diagnose. Use wording like "can be linked to", "may point toward", "worth discussing with your doctor".
- Never recommend medicines, doses or treatments.
- Do not say a result is fine unless the facts say NORMAL.
- Keep test names, numbers and units exactly as given, even when writing in another language.
- connect_the_dots: mention a pattern only if EVERY result it depends on appears in the facts. Otherwise leave it empty.
- Do not repeat what the doctor's report already says in different words; explain what it means.
- Keep the tone calm and warm. Do not frighten the reader.
- key_points: include EVERY item — normal, abnormal, and unclear alike. For a normal value, give a short,
  reassuring one-line note in plain language (e.g. "this is right where it should be — nothing to worry about
  here"), not just the number restated.
- For imaging, ECG or pathology findings, explain what the finding means in plain language. Never say "this measures".
- Never suggest an abnormal finding is normal, harmless or age-related unless the report itself says so. If the
  report says something is more than expected, say so plainly, in simple words."""


class ExplainedReport(BaseModel):
    urgency: str  # urgent / see_doctor_soon / routine_followup / all_normal
    urgency_reason: str
    explanation: Explanation
    disclaimer: str = DISCLAIMER


def compute_urgency(result: AnalysisResult) -> tuple[str, str]:
    n = result.narrative
    if n and n.urgent_language:
        return "urgent", f'The report itself uses urgent wording: "{n.urgent_language}"'

    marked = [c.name for c in result.checked_values if c.severity == "marked"]
    if marked:
        return "see_doctor_soon", ("These results are well outside the report's printed range: "
                                   + ", ".join(marked) + ". Worth discussing with your doctor soon.")

    abnormal_labs = [c for c in result.checked_values if c.status in ("low", "high")]
    abnormal_findings = [f for f in (n.findings if n else []) if f.significance == "abnormal"]
    if abnormal_labs:
        return "routine_followup", "Some results are outside the normal range. Discuss them at your next visit."
    if abnormal_findings:
        return "routine_followup", ("The report describes findings that are worth reviewing with your doctor. "
                                    "Please book a visit to go through them.")

    return "all_normal", "Nothing in this report is marked outside the normal range."


def _range_text(low, high) -> str:
    if low is not None and high is not None:
        return f" (printed range {low} - {high})"
    if high is not None:
        return f" (printed range up to {high})"
    if low is not None:
        return f" (printed range at least {low})"
    return ""


def build_facts(result: AnalysisResult) -> str:
    r = result.report
    lines = [
        f"Report type: {r.report_type.value}",
        f"Age: {r.patient_age or 'not stated'}",
        f"Sex: {r.patient_sex or 'not stated'}",
    ]
    if result.checked_values:
        lines.append("\nLAB VALUES (status decided by software using the report's own printed ranges):")
        for c in result.checked_values:
            detail = c.status.upper()
            if c.severity:
                detail += f", {c.severity}, {c.deviation_pct}% outside range"
            lines.append(f"- {c.name}: {c.value_text} {c.unit or ''} -> {detail}{_range_text(c.low, c.high)}")
    n = result.narrative
    if n:
        lines.append(f"\nREPORT: {n.modality}")
        if n.indication:
            lines.append(f"Reason for test: {n.indication}")
        for f in n.findings:
            lines.append(f"- [{f.significance.upper()}] {f.body_part or ''}: {f.finding}")
        if n.impression:
            lines.append(f"Doctor's impression: {n.impression}")
        if n.recommendations_in_report:
            lines.append("Advice printed in the report: " + "; ".join(n.recommendations_in_report))
    return "\n".join(lines)


def explain(result: AnalysisResult, language: str = "English",
            llm: LLMClient | None = None) -> ExplainedReport:
    llm = llm or LLMClient()
    urgency, reason = compute_urgency(result)
    prompt = (
        f"Write in {language}.\n"
        f"Overall urgency (already decided, do not change it): {urgency}\n\n"
        f"FACTS:\n{build_facts(result)}"
    )
    explanation = llm.generate_structured(prompt, schema=Explanation, system=SYSTEM_PROMPT)
    return ExplainedReport(urgency=urgency, urgency_reason=reason, explanation=explanation)