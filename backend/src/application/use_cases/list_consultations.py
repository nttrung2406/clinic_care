from dataclasses import dataclass

from src.domain.entities import Consultation
from src.domain.ports import ConsultationRepository


@dataclass
class ListConsultations:
    repository: ConsultationRepository

    def execute(
        self, patient: str | None = None, diagnosis_code: str | None = None
    ) -> list[Consultation]:
        return self.repository.list(patient=patient, diagnosis_code=diagnosis_code)
