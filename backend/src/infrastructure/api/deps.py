from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from src.application.use_cases.authenticate_doctor import AuthenticateDoctor
from src.application.use_cases.create_consultation import CreateConsultation
from src.application.use_cases.list_consultations import ListConsultations
from src.application.use_cases.search_diagnosis_codes import SearchDiagnosisCodes
from src.config import get_settings
from src.infrastructure.db.repositories import (
    SqlConsultationRepository,
    SqlDiagnosisRepository,
    SqlDoctorRepository,
)
from src.infrastructure.db.session import get_session
from src.infrastructure.security.password import BcryptPasswordHasher
from src.infrastructure.security.tokens import JwtTokenIssuer

_bearer_scheme = HTTPBearer(auto_error=False)


def get_diagnosis_repository(session: Session = Depends(get_session)) -> SqlDiagnosisRepository:
    return SqlDiagnosisRepository(session)


def get_consultation_repository(
    session: Session = Depends(get_session),
) -> SqlConsultationRepository:
    return SqlConsultationRepository(session)


def get_doctor_repository(session: Session = Depends(get_session)) -> SqlDoctorRepository:
    return SqlDoctorRepository(session)


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


def get_token_issuer() -> JwtTokenIssuer:
    settings = get_settings()
    return JwtTokenIssuer(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.jwt_expires_minutes,
    )


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


def get_authenticate_doctor_use_case(
    doctors: SqlDoctorRepository = Depends(get_doctor_repository),
    hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    tokens: JwtTokenIssuer = Depends(get_token_issuer),
) -> AuthenticateDoctor:
    return AuthenticateDoctor(doctors=doctors, hasher=hasher, tokens=tokens)


def get_current_doctor(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    tokens: JwtTokenIssuer = Depends(get_token_issuer),
) -> str:
    """Verify the bearer JWT and return the authenticated doctor's username."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = tokens.decode(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return payload["username"]

