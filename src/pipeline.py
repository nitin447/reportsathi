from pydantic import BaseModel

from src.extractor import extract_narrative, extract_report
from src.flagger import CheckedValue, check_report
from src.llm import LLMClient
from src.schemas import ExtractedReport, NarrativeReport, ReportType

NARRATIVE_TYPES = {ReportType.imaging, ReportType.ecg, ReportType.pathology}


class AnalysisResult(BaseModel):
    report: ExtractedReport
    checked_values: list[CheckedValue] = []
    narrative: NarrativeReport | None = None


def analyze(file_path: str, llm: LLMClient | None = None) -> AnalysisResult:
    llm = llm or LLMClient()
    report = extract_report(file_path, llm)
    checked = check_report(report)  # works when numbers are present (blood tests, ECG measurements)

    narrative = None
    if report.report_type in NARRATIVE_TYPES or report.narrative_findings:
        narrative = extract_narrative(file_path, llm)

    return AnalysisResult(report=report, checked_values=checked, narrative=narrative)