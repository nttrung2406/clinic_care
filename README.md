# ClinicCare Mini EMR

A minimal, secure tool for clinics to record diagnosis codes and consultation notes.

Doctors can:
1. Search ICD-10 diagnosis codes.
2. Record a consultation note with one or more selected diagnosis codes.
3. List past consultation notes.
4. Search past notes by patient name or diagnosis code.

See [requirements.md](requirements.md) for the full product brief.

## Architecture

```
clinic_care/
├── database/     # Postgres + Alembic migrations (schema & seed data)
├── backend/      # FastAPI service (hexagonal architecture)
├── frontend/     # Nuxt 3 app
├── codes.txt     # Source ICD-10 (code, description) dataset, seeded into Postgres
└── start.sh      # Orchestrates database, migrations, backend, frontend
```

### Database (`database/`)

- Postgres 16, run via `database/docker-compose.yml` (service `postgres`, container `clinic_care_postgres`).
- Schema and data are managed by Alembic migrations in `database/migrations/versions/`:
  - `202608190001_...` creates `diagnosis_codes`, `consultations`, and the `consultation_diagnosis_codes` join table.
  - `202608190002_...` seeds `diagnosis_codes` with the ICD-10 rows from [codes.txt](codes.txt).
- Alembic itself lives in `backend/` ([backend/alembic.ini](backend/alembic.ini)) since it needs the Python/SQLAlchemy toolchain, but `script_location` points at `database/migrations` so the migration history stays with the database stack.

### Backend (`backend/`)

FastAPI service built with a hexagonal (ports & adapters) architecture under `backend/src/`:

- `domain/` — framework-agnostic core: entities (`DiagnosisCode`, `Consultation`), repository ports (`DiagnosisRepository`, `ConsultationRepository`), domain exceptions.
- `application/use_cases/` — orchestration logic (`SearchDiagnosisCodes`, `CreateConsultation`, `ListConsultations`), depends only on the domain ports.
- `infrastructure/db/` — outbound adapters: SQLModel table models, Postgres session/engine, SQL repository implementations.
- `infrastructure/api/` — inbound adapter: Pydantic request/response schemas, FastAPI dependency wiring, routers.
- `app.py` / `main.py` — FastAPI app factory and entrypoint.

**Endpoints**

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET | `/diagnosis?search=<term>&limit=` | Search ICD-10 diagnosis codes by code or description |
| POST | `/consultation` | Create a consultation note with `patient_name`, `notes`, `diagnosis_codes[]` (422 if a code doesn't exist) |
| GET | `/consultation?patient=&diagnosis_code=` | List/search past consultations by patient name or diagnosis code |


### Frontend (`frontend/`)

Nuxt 3 app with three pages, calling the backend through `composables/useDiagnosisApi.ts` and `composables/useConsultationApi.ts`:

- `pages/consultations/index.vue` — table of past consultations.
- `pages/consultations/new.vue` — new consultation form with a diagnosis code picker (`components/DiagnosisCodePicker.vue`).
- `pages/search.vue` — search consultations by patient or diagnosis code.

The API base URL is configured via `NUXT_PUBLIC_API_BASE` (defaults to `http://localhost:8090`). Runs on port `3000`.

## Prerequisites

- Docker + Docker Compose
- Node.js (for the frontend)
- `bash`

## Setup

1. Copy environment files and adjust as needed:

   ```bash
   cp database/.env.example database/.env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

   Make sure `backend/.env`'s `DATABASE_URL` password matches `database/.env`'s `POSTGRES_PASSWORD`.

2. Start everything (creates the shared Docker network, starts Postgres, runs migrations, then starts the backend and frontend):

   ```bash
   ./start.sh
   ```

   - Backend: http://localhost:8090 (docs at `/docs`)
   - Frontend: http://localhost:3000

## `start.sh` usage

```bash
./start.sh                          # same as `up`
./start.sh up                       # start db, run migrations, start backend + frontend
./start.sh migrate                  # run database migrations only
./start.sh logs db [-f]             # tail Postgres logs
./start.sh logs backend [-f]        # tail backend container logs
./start.sh logs frontend [-f]       # tail frontend dev server logs
./start.sh help                     # show usage
```

The frontend runs as a background `npm run dev` process; its output is written to `logs/frontend.log` and its PID to `logs/frontend.pid`.

## Development notes

- New DB schema changes: add an Alembic revision under `database/migrations/versions/` (see `backend/alembic.ini` for config), then run `./start.sh migrate`.
- Backend dependencies are managed with `uv` via `backend/pyproject.toml`.
- Frontend dependencies are managed with `npm` via `frontend/package.json`.
