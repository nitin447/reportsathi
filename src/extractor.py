from src.llm import LLMClient
from src.schemas import ExtractedReport

SYSTEM_PROMPT = """You extract data from medical reports.
Rules:
- Copy values, units and reference ranges EXACTLY as printed. Never guess or correct them.
- If something is unreadable or missing, use null.
- Do NOT extract the patient's name, phone number, address, ID or doctor names.
- Only fill flag_in_report if the report itself prints a flag (H, L, High, Low, etc.).
- For imaging, ECG or pathology reports, put the findings/impression in narrative_findings.
- Include every test row you can find."""


def extract_report(file_path: str, llm: LLMClient | None = None) -> ExtractedReport:
    llm = llm or LLMClient()
    return llm.generate_structured_from_file(
        file_path=file_path,
        prompt="Extract this medical report.",
        schema=ExtractedReport,
        system=SYSTEM_PROMPT,
    )