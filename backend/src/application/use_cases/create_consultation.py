from dataclasses import dataclass

from src.domain.entities import Consultation
from src.domain.exceptions import UnknownDiagnosisCodeError
from src.domain.ports import ConsultationRepository, DiagnosisRepository


@dataclass
class CreateConsultation:
    consultations: ConsultationRepository
    diagnoses: DiagnosisRepository

    def execute(self, consultation: Consultation) -> Consultation:
        requested = set(consultation.diagnosis_codes)
        existing = self.diagnoses.existing_codes(list(requested))
        missing = requested - existing
        if missing:
            raise UnknownDiagnosisCodeError(sorted(missing))
        return self.consultations.add(consultation)
