from fastapi import Depends
from sqlmodel import Session

from src.application.use_cases.create_consultation import CreateConsultation
from src.application.use_cases.list_consultations import ListConsultations
from src.application.use_cases.search_diagnosis_codes import SearchDiagnosisCodes
from src.infrastructure.db.repositories import SqlConsultationRepository, SqlDiagnosisRepository
from src.infrastructure.db.session import get_session


def get_diagnosis_repository(session: Session = Depends(get_session)) -> SqlDiagnosisRepository:
    return SqlDiagnosisRepository(session)


def get_consultation_repository(
    session: Session = Depends(get_session),
) -> SqlConsultationRepository:
    return SqlConsultationRepository(session)


def get_search_diagnosis_codes_use_case(
    repository: SqlDiagnosisRepository = Depends(get_diagnosis_repository),
) -> SearchDiagnosisCodes:
    return SearchDiagnosisCodes(repository=repository)


def get_create_consultation_use_case(
    consultations: SqlConsultationRepository = Depends(get_consultation_repository),
    diagnoses: SqlDiagnosisRepository = Depends(get_diagnosis_repository),
) -> CreateConsultation:
    return CreateConsultation(consultations=consultations, diagnoses=diagnoses)


def get_list_consultations_use_case(
    repository: SqlConsultationRepository = Depends(get_consultation_repository),
) -> ListConsultations:
    return ListConsultations(repository=repository)
