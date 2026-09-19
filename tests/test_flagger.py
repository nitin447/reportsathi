from src.flagger import parse_range, pick_range_text, check_value
from src.schemas import LabValue


def test_range_dash():
    assert parse_range("12.0 - 15.5") == (12.0, 15.5)


def test_range_with_commas():
    assert parse_range("4,000 - 11,000") == (4000.0, 11000.0)


def test_range_less_than():
    assert parse_range("< 200") == (None, 200.0)


def test_range_greater_than():
    assert parse_range("> 40") == (40.0, None)


def test_low_hemoglobin_using_report_range():
    v = LabValue(name="Hemoglobin", value_text="10.2", value_numeric=10.2,
                 unit="g/dL", reference_range_text="12.0 - 15.5", flag_in_report="L")
    r = check_value(v, "female")
    assert r.status == "low"
    assert r.range_source == "report"
    assert r.matches_report_flag is True


def test_platelets_in_lakh_need_no_conversion():
    v = LabValue(name="Platelet Count", value_text="2.4", value_numeric=2.4,
                 unit="lakh/cumm", reference_range_text="1.5 - 4.5")
    assert check_value(v).status == "normal"


def test_sex_specific_range_female():
    txt = "Male: 13.0 - 17.0 Female: 12.0 - 15.5"
    assert parse_range(pick_range_text(txt, "female")[0]) == (12.0, 15.5)


def test_sex_specific_range_male():
    txt = "Male: 13.0 - 17.0 Female: 12.0 - 15.5"
    assert parse_range(pick_range_text(txt, "male")[0]) == (13.0, 17.0)


def test_sex_specific_range_unknown_sex_is_not_guessed():
    v = LabValue(name="Hemoglobin", value_text="12.5", value_numeric=12.5, unit="g/dL",
                 reference_range_text="Male: 13.0 - 17.0 Female: 12.0 - 15.5")
    r = check_value(v, None)
    assert r.status == "unknown"


def test_no_range_uses_report_flag():
    v = LabValue(name="Hb", value_text="9", value_numeric=9.0, unit="g/dL", flag_in_report="L")
    r = check_value(v)
    assert r.status == "low"
    assert r.range_source == "report_flag"


def test_no_range_no_flag_is_unknown():
    v = LabValue(name="Hb", value_text="9", value_numeric=9.0, unit="g/dL")
    assert check_value(v).status == "unknown"


def test_report_flag_mismatch_is_detected():
    v = LabValue(name="MCV", value_text="72", value_numeric=72.0,
                 unit="fL", reference_range_text="80 - 100", flag_in_report=None)
    r = check_value(v)
    assert r.status == "low"
    assert r.matches_report_flag is False