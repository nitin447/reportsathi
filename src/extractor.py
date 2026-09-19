from src.llm import LLMClient
from src.schemas import ExtractedReport, NarrativeReport

SYSTEM_PROMPT = """You extract data from medical reports.
Rules:
- Copy values, units and reference ranges EXACTLY as printed. Never guess or correct them.
- If something is unreadable or missing, use null.
- Do NOT extract the patient's name, phone number, address, ID or doctor names.
- Only fill flag_in_report if the report itself prints a flag (H, L, High, Low, etc.).
- For imaging, ECG or pathology reports, put the findings/impression in narrative_findings.
- Include every test row you can find."""

NARRATIVE_PROMPT = """You extract findings from narrative medical reports (imaging, ECG, pathology).
Rules:
- Use ONLY what the report says. Do not interpret, diagnose, or add anything.
- Do NOT extract the patient's name, phone number, address, ID or doctor names.
- Set significance only from the report's own wording. If unclear, use 'unclear'.
- Copy the impression exactly as printed.
- recommendations_in_report must contain only advice actually printed in the report.
- Fill urgent_language only if the report itself uses urgent/immediate/critical wording.
- Keep the report's hedging and cause wording (presumably, probably, likely, possibly, suggestive of, due to) inside each finding. Never drop it or shorten a finding so that it sounds more certain or less certain than the report."""


def extract_report(file_path: str, llm: LLMClient | None = None) -> ExtractedReport:
    llm = llm or LLMClient()
    return llm.generate_structured_from_file(
        file_path=file_path,
        prompt="Extract this medical report.",
        schema=ExtractedReport,
        system=SYSTEM_PROMPT,
    )


def extract_narrative(file_path: str, llm: LLMClient | None = None) -> NarrativeReport:
    llm = llm or LLMClient()
    return llm.generate_structured_from_file(
        file_path=file_path,
        prompt="Extract the findings from this report.",
        schema=NarrativeReport,
        system=NARRATIVE_PROMPT,
    )