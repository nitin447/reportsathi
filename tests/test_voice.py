from src.explainer import ExplainedReport
from src.schemas import Explanation, KeyPoint
from src.voice import CLOSING, MAX_CHARS, build_spoken_script


def make(summary, points):
    return ExplainedReport(
        urgency="routine_followup", urgency_reason="x",
        explanation=Explanation(summary=summary, key_points=points,
                                connect_the_dots=[], questions_for_doctor=[]))


def test_short_script_has_summary_points_and_closing():
    e = make("Your hemoglobin is low.", [KeyPoint(name="Hemoglobin", status="low", meaning="Carries oxygen.")])
    s = build_spoken_script(e, "English")
    assert "Your hemoglobin is low." in s
    assert "Hemoglobin. Carries oxygen." in s
    assert s.endswith(CLOSING["English"])


def test_long_script_stays_under_limit_and_keeps_closing():
    points = [KeyPoint(name=f"Test {i}", status="low", meaning="word " * 60) for i in range(30)]
    e = make("Summary here.", points)
    s = build_spoken_script(e, "Hindi")
    assert len(s) <= MAX_CHARS
    assert s.endswith(CLOSING["Hindi"])