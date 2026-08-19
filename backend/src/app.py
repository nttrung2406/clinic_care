from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.domain.exceptions import DomainError
from src.infrastructure.api.routers import consultation, diagnosis, health


def create_app() -> FastAPI:
    app = FastAPI(title="ClinicCare Mini EMR", version="1.0.0")

    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(DomainError)
    def handle_domain_error(_: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    app.include_router(health.router)
    app.include_router(diagnosis.router)
    app.include_router(consultation.router)

    return app


app = create_app()
