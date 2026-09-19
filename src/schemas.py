from enum import Enum
from typing import Literal

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
class Finding(BaseModel):
    body_part: str | None = Field(default=None, description="Organ or region this finding is about")
    finding: str = Field(description="The finding, short, using the report's own wording")
    significance: Literal["normal", "abnormal", "borderline", "incidental", "unclear"] = Field(
        description="Decide ONLY from the report's wording, e.g. 'no abnormality' = normal, "
                    "'mild bulge' = abnormal. If the wording doesn't make it clear, use 'unclear'."
    )


class NarrativeReport(BaseModel):
    modality: str = Field(description="e.g. MRI Lumbar Spine, Chest X-ray, Ultrasound Abdomen, ECG, Biopsy")
    indication: str | None = Field(default=None, description="Reason for the test / clinical history, if printed")
    findings: list[Finding] = Field(default_factory=list)
    impression: str | None = Field(default=None, description="The report's impression / conclusion, copied as printed")
    recommendations_in_report: list[str] = Field(
        default_factory=list, description="Follow-up advice printed in the report itself. Never add your own."
    )
    urgent_language: str | None = Field(
        default=None, description="Exact phrase if the report says urgent / immediate / critical. Otherwise null."
    )