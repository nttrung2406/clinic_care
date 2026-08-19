from datetime import datetime

from sqlmodel import Field, SQLModel


class DiagnosisCodeModel(SQLModel, table=True):
    __tablename__ = "diagnosis_codes"

    code: str = Field(primary_key=True, max_length=10)
    description: str


class ConsultationModel(SQLModel, table=True):
    __tablename__ = "consultations"

    id: int | None = Field(default=None, primary_key=True)
    patient_name: str = Field(max_length=200, index=True)
    notes: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConsultationDiagnosisCodeModel(SQLModel, table=True):
    __tablename__ = "consultation_diagnosis_codes"

    consultation_id: int = Field(foreign_key="consultations.id", primary_key=True)
    diagnosis_code: str = Field(foreign_key="diagnosis_codes.code", primary_key=True, max_length=10)


class DoctorModel(SQLModel, table=True):
    __tablename__ = "doctors"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
