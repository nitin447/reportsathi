from src.explainer import compute_urgency
from src.flagger import check_value
from src.pipeline import AnalysisResult
from src.schemas import ExtractedReport, Finding, LabValue, NarrativeReport, ReportType

def make(values, narrative=None, rtype=ReportType.blood_count):
    report = ExtractedReport(report_type=rtype, values=values)
    return AnalysisResult(report=report,
                          checked_values=[check_value(v) for v in values],
                          narrative=narrative)


def hb(value):
    return LabValue(name="Hb", value_text=str(value), value_numeric=float(value),
                    unit="g/dL", reference_range_text="12 - 16")


def test_all_normal():
    assert compute_urgency(make([hb(14)]))[0] == "all_normal"


def test_mildly_low_is_routine():
    assert compute_urgency(make([hb(11.5)]))[0] == "routine_followup"


def test_far_outside_range_is_see_doctor_soon():
    assert compute_urgency(make([hb(6)]))[0] == "see_doctor_soon"


def test_urgent_wording_in_report_is_urgent():
    n = NarrativeReport(modality="Chest X-ray", urgent_language="Urgent clinical attention advised")
    r = make([], narrative=n, rtype=ReportType.imaging)
    assert compute_urgency(r)[0] == "urgent"
def test_abnormal_imaging_finding_uses_findings_wording():
    n = NarrativeReport(modality="MRI", findings=[Finding(finding="Disc bulge", significance="abnormal")])
    r = make([], narrative=n, rtype=ReportType.imaging)
    level, reason = compute_urgency(r)
    assert level == "routine_followup"
    assert "findings" in reason