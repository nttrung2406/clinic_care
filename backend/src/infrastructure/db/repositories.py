from sqlalchemy import or_
from sqlmodel import Session, select

from src.domain.entities import Consultation, DiagnosisCode
from src.infrastructure.db.models import (
    ConsultationDiagnosisCodeModel,
    ConsultationModel,
    DiagnosisCodeModel,
)


class SqlDiagnosisRepository:
    def __init__(self, session: Session):
        self.session = session

    def search(self, term: str | None, limit: int = 50) -> list[DiagnosisCode]:
        statement = select(DiagnosisCodeModel)
        if term:
            like = f"%{term}%"
            statement = statement.where(
                or_(
                    DiagnosisCodeModel.code.ilike(like),
                    DiagnosisCodeModel.description.ilike(like),
                )
            )
        statement = statement.order_by(DiagnosisCodeModel.code).limit(limit)
        rows = self.session.exec(statement).all()
        return [DiagnosisCode(code=row.code, description=row.description) for row in rows]

    def existing_codes(self, codes: list[str]) -> set[str]:
        if not codes:
            return set()
        statement = select(DiagnosisCodeModel.code).where(DiagnosisCodeModel.code.in_(codes))
        return set(self.session.exec(statement).all())


class SqlConsultationRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, consultation: Consultation) -> Consultation:
        model = ConsultationModel(patient_name=consultation.patient_name, notes=consultation.notes)
        self.session.add(model)
        self.session.flush()  # assign model.id before creating the join rows

        for code in consultation.diagnosis_codes:
            self.session.add(
                ConsultationDiagnosisCodeModel(consultation_id=model.id, diagnosis_code=code)
            )

        self.session.commit()
        self.session.refresh(model)

        return Consultation(
            id=model.id,
            patient_name=model.patient_name,
            notes=model.notes,
            diagnosis_codes=consultation.diagnosis_codes,
            created_at=model.created_at,
        )

    def list(
        self, patient: str | None = None, diagnosis_code: str | None = None
    ) -> list[Consultation]:
        statement = select(ConsultationModel)
        if patient:
            statement = statement.where(ConsultationModel.patient_name.ilike(f"%{patient}%"))
        if diagnosis_code:
            statement = statement.join(
                ConsultationDiagnosisCodeModel,
                ConsultationDiagnosisCodeModel.consultation_id == ConsultationModel.id,
            ).where(ConsultationDiagnosisCodeModel.diagnosis_code == diagnosis_code)
        statement = statement.order_by(ConsultationModel.created_at.desc())

        rows = self.session.exec(statement).all()

        results = []
        for row in rows:
            codes_statement = select(ConsultationDiagnosisCodeModel.diagnosis_code).where(
                ConsultationDiagnosisCodeModel.consultation_id == row.id
            )
            codes = list(self.session.exec(codes_statement).all())
            results.append(
                Consultation(
                    id=row.id,
                    patient_name=row.patient_name,
                    notes=row.notes,
                    diagnosis_codes=codes,
                    created_at=row.created_at,
                )
            )
        return results
