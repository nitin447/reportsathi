import re

from pydantic import BaseModel

from src.schemas import ExtractedReport, LabValue

_NUM = r"(\d+(?:\.\d+)?)"


def parse_range(text: str | None):
    """'12.0 - 15.5' -> (12.0, 15.5); '< 200' -> (None, 200.0); '> 40' -> (40.0, None)."""
    if not text:
        return None
    t = text.lower().replace(",", "").replace("–", "-").replace("—", "-")
    m = re.search(_NUM + r"\s*(?:-|to)\s*" + _NUM, t)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        if lo <= hi:
            return lo, hi
    m = re.search(r"(?:<=|<|less than|up to|upto|below)\s*" + _NUM, t)
    if m:
        return None, float(m.group(1))
    m = re.search(r"(?:>=|>|greater than|more than|above)\s*" + _NUM, t)
    if m:
        return float(m.group(1)), None
    return None


def pick_range_text(text: str, sex: str | None):
    """If the report prints separate male/female ranges, pick the right one."""
    t = text.lower()
    marks = [(m.start(), m.group()) for m in re.finditer(r"\b(female|male)\b", t)]
    if len({g for _, g in marks}) < 2:
        return text, None
    if sex not in ("male", "female"):
        return None, "The report prints separate ranges for males and females, but the patient's sex is not stated."
    for i, (pos, g) in enumerate(marks):
        if g == sex:
            end = marks[i + 1][0] if i + 1 < len(marks) else len(t)
            return t[pos:end], None
    return None, None


def _flag_to_status(flag: str | None):
    if not flag:
        return None
    f = flag.strip().lower()
    if f in ("h", "hh", "*h", "↑") or f.startswith("high"):
        return "high"
    if f in ("l", "ll", "*l", "↓") or f.startswith("low"):
        return "low"
    return None


class CheckedValue(BaseModel):
    name: str
    value_text: str
    unit: str | None
    status: str  # low / high / normal / unknown / not_numeric
    low: float | None
    high: float | None
    range_source: str  # report / report_flag / none
    deviation_pct: float | None
    severity: str | None  # mild / moderate / marked
    matches_report_flag: bool | None
    note: str | None


def check_value(v: LabValue, sex: str | None = None) -> CheckedValue:
    def build(**kw):
        base = dict(name=v.name, value_text=v.value_text, unit=v.unit, status="unknown",
                    low=None, high=None, range_source="none", deviation_pct=None,
                    severity=None, matches_report_flag=None, note=None)
        base.update(kw)
        return CheckedValue(**base)

    if v.value_numeric is None:
        return build(status="not_numeric")

    num = v.value_numeric
    note = None

    range_text, range_note = (None, None)
    if v.reference_range_text:
        range_text, range_note = pick_range_text(v.reference_range_text, sex)
    parsed = parse_range(range_text)

    # Case 1: the report printed a usable range
    if parsed:
        low, high = parsed
        if low is not None and num < low:
            status = "low"
        elif high is not None and num > high:
            status = "high"
        else:
            status = "normal"

        dev = sev = None
        if status == "low" and low:
            dev = round((low - num) / low * 100, 1)
        elif status == "high" and high:
            dev = round((num - high) / high * 100, 1)
        if dev is not None:
            sev = "mild" if dev < 10 else "moderate" if dev < 30 else "marked"

        matches = None
        rf = _flag_to_status(v.flag_in_report)
        if rf is not None or not v.flag_in_report:
            matches = (rf or "normal") == status
            if not matches:
                note = "Report flag disagrees with our check. Please verify this value."

        return build(status=status, low=low, high=high, range_source="report",
                     deviation_pct=dev, severity=sev, matches_report_flag=matches, note=note)

    # Case 2: no usable range, but the report itself printed a flag
    rf = _flag_to_status(v.flag_in_report)
    if rf:
        return build(status=rf, range_source="report_flag",
                     note=range_note or "No reference range printed. Using the report's own flag.")

    # Case 3: nothing to compare against
    return build(status="unknown",
                 note=range_note or "No reference range printed in the report, so this value can't be judged.")


def check_report(report: ExtractedReport) -> list[CheckedValue]:
    sex = (report.patient_sex or "").lower() or None
    return [check_value(v, sex) for v in report.values]