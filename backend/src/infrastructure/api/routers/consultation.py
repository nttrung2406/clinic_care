from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.use_cases.create_consultation import CreateConsultation
from src.application.use_cases.list_consultations import ListConsultations
from src.domain.entities import Consultation
from src.domain.exceptions import UnknownDiagnosisCodeError
from src.infrastructure.api.deps import (
    get_create_consultation_use_case,
    get_current_doctor,
    get_list_consultations_use_case,
)
from src.infrastructure.api.schemas import ConsultationCreate, ConsultationOut

router = APIRouter(
    prefix="/consultation", tags=["consultation"], dependencies=[Depends(get_current_doctor)]
)


def _to_out(consultation: Consultation) -> ConsultationOut:
    return ConsultationOut(
        id=consultation.id,
        patient_name=consultation.patient_name,
        notes=consultation.notes,
        diagnosis_codes=consultation.diagnosis_codes,
        created_at=consultation.created_at,
    )


@router.post("", response_model=ConsultationOut, status_code=status.HTTP_201_CREATED)
def create_consultation(
    payload: ConsultationCreate,
    use_case: CreateConsultation = Depends(get_create_consultation_use_case),
) -> ConsultationOut:
    try:
        consultation = use_case.execute(
            Consultation(
                patient_name=payload.patient_name,
                notes=payload.notes,
                diagnosis_codes=payload.diagnosis_codes,
            )
        )
    except UnknownDiagnosisCodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
    return _to_out(consultation)


@router.get("", response_model=list[ConsultationOut])
def list_consultations(
    patient: str | None = Query(default=None, min_length=1, max_length=200),
    diagnosis_code: str | None = Query(default=None, min_length=1, max_length=10),
    use_case: ListConsultations = Depends(get_list_consultations_use_case),
) -> list[ConsultationOut]:
    results = use_case.execute(patient=patient, diagnosis_code=diagnosis_code)
    return [_to_out(item) for item in results]
