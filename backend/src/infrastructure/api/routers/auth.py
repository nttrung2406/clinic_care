from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.authenticate_doctor import AuthenticateDoctor
from src.domain.exceptions import InvalidCredentialsError
from src.infrastructure.api.deps import get_authenticate_doctor_use_case
from src.infrastructure.api.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    use_case: AuthenticateDoctor = Depends(get_authenticate_doctor_use_case),
) -> LoginResponse:
    try:
        token = use_case.execute(payload.username, payload.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc
    return LoginResponse(access_token=token)
