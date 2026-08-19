"""Ports: interfaces the application layer depends on, implemented by infrastructure adapters."""

from typing import Protocol

from src.domain.entities import Consultation, DiagnosisCode, Doctor


class DiagnosisRepository(Protocol):
    def search(self, term: str | None, limit: int = 50) -> list[DiagnosisCode]: ...

    def existing_codes(self, codes: list[str]) -> set[str]: ...


class ConsultationRepository(Protocol):
    def add(self, consultation: Consultation) -> Consultation: ...

    def list(
        self, patient: str | None = None, diagnosis_code: str | None = None
    ) -> list[Consultation]: ...


class DoctorRepository(Protocol):
    def get_by_username(self, username: str) -> Doctor | None: ...


class PasswordHasher(Protocol):
    def verify(self, password: str, password_hash: str) -> bool: ...


class TokenIssuer(Protocol):
    def issue(self, doctor: Doctor) -> str: ...
