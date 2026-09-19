from src.explainer import ExplainedReport
from src.flagger import check_value
from src.pdf_report import build_pdf
from src.pipeline import AnalysisResult
from src.schemas import Explanation, ExtractedReport, KeyPoint, LabValue, ReportType


def make(name):
    values = [LabValue(name=name, value_text="10.2", value_numeric=10.2, unit="g/dL",
                       reference_range_text="12.0 - 15.5", flag_in_report="L")]
    report = ExtractedReport(report_type=ReportType.blood_count, patient_age=28,
                             patient_sex="female", values=values)
    result = AnalysisResult(report=report, checked_values=[check_value(v, "female") for v in values])
    explained = ExplainedReport(
        urgency="routine_followup", urgency_reason="Some results are outside the normal range.",
        explanation=Explanation(
            summary="Your hemoglobin is a little low.",
            key_points=[KeyPoint(name=name, status="low", meaning="Carries oxygen.")],
            connect_the_dots=[], questions_for_doctor=["What might cause this?"]))
    return result, explained


def test_pdf_is_created(tmp_path):
    result, explained = make("Hemoglobin")
    out = tmp_path / "summary.pdf"
    build_pdf(result, explained, str(out))
    assert out.exists() and out.stat().st_size > 1000


def test_pdf_handles_special_characters(tmp_path):
    result, explained = make("Vitamin B12 & D <test>")
    out = tmp_path / "summary2.pdf"
    build_pdf(result, explained, str(out))
    assert out.exists()