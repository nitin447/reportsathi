from enum import Enum

from pydantic import BaseModel, Field


class ReportType(str, Enum):
    blood_count = "blood_count"
    biochemistry = "biochemistry"
    lipid = "lipid"
    thyroid = "thyroid"
    liver = "liver"
    kidney = "kidney"
    diabetes = "diabetes"
    vitamins_minerals = "vitamins_minerals"
    urine = "urine"
    imaging = "imaging"
    ecg = "ecg"
    pathology = "pathology"
    other = "other"


class LabValue(BaseModel):
    name: str = Field(description="Test name exactly as printed")
    value_text: str = Field(description="Result exactly as printed")
    value_numeric: float | None = Field(default=None, description="Number if the result is numeric, else null")
    unit: str | None = None
    reference_range_text: str | None = Field(default=None, description="Reference range exactly as printed")
    flag_in_report: str | None = Field(default=None, description="H, L, High, Low, Abnormal etc. only if printed in the report")


class ExtractedReport(BaseModel):
    report_type: ReportType
    report_date: str | None = None
    patient_age: int | None = None
    patient_sex: str | None = Field(default=None, description="male, female or null")
    values: list[LabValue] = Field(default_factory=list)
    narrative_findings: str | None = Field(
        default=None,
        description="For imaging, ECG or pathology reports: the findings/impression text",
    )