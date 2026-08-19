#!/bin/bash
set -e

/opt/venv/bin/python -m alembic upgrade head

exec /opt/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8090 --reload