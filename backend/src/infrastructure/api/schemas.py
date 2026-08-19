from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class DiagnosisCodeOut(BaseModel):
    code: str
    description: str


class ConsultationCreate(BaseModel):
    patient_name: str = Field(min_length=1, max_length=200)
    notes: str = Field(min_length=1)
    diagnosis_codes: list[str] = Field(min_length=1)

    @field_validator("diagnosis_codes")
    @classmethod
    def normalize_diagnosis_codes(cls, value: list[str]) -> list[str]:
        codes = [code.strip().upper() for code in value if code.strip()]
        if not codes:
            raise ValueError("at least one diagnosis code is required")
        return codes


class ConsultationOut(BaseModel):
    id: int
    patient_name: str
    notes: str
    diagnosis_codes: list[str]
    created_at: datetime
