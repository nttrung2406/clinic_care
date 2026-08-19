from fastapi import APIRouter, Depends, Query

from src.application.use_cases.search_diagnosis_codes import SearchDiagnosisCodes
from src.infrastructure.api.deps import get_current_doctor, get_search_diagnosis_codes_use_case
from src.infrastructure.api.schemas import DiagnosisCodeOut

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"], dependencies=[Depends(get_current_doctor)])


@router.get("", response_model=list[DiagnosisCodeOut])
def search_diagnosis_codes(
    search: str | None = Query(default=None, min_length=1, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    use_case: SearchDiagnosisCodes = Depends(get_search_diagnosis_codes_use_case),
) -> list[DiagnosisCodeOut]:
    results = use_case.execute(term=search, limit=limit)
    return [DiagnosisCodeOut(code=item.code, description=item.description) for item in results]
