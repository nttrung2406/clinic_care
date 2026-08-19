"""Framework-agnostic domain entities (no FastAPI/SQLModel imports here)."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class DiagnosisCode:
    code: str
    description: str


@dataclass
class Consultation:
    patient_name: str
    notes: str
    diagnosis_codes: list[str] = field(default_factory=list)
    id: int | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class Doctor:
    id: int
    username: str
    password_hash: str
