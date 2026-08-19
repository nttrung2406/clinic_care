#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
FRONTEND_LOG="$LOG_DIR/frontend.log"
FRONTEND_PID_FILE="$LOG_DIR/frontend.pid"
DB_COMPOSE=(docker compose -f "$ROOT_DIR/database/docker-compose.yml")
BACKEND_COMPOSE=(docker compose -f "$ROOT_DIR/backend/docker-compose.dev.yml")

ensure_network() {
  docker network inspect clinic_care_network >/dev/null 2>&1 || \
    docker network create clinic_care_network
}

start_database() {
  echo "==> Starting database service"
  "${DB_COMPOSE[@]}" up -d
}

wait_for_database() {
  echo "==> Waiting for postgres to become healthy"
  for _ in $(seq 1 30); do
    status="$(docker inspect -f '{{.State.Health.Status}}' clinic_care_postgres 2>/dev/null || echo starting)"
    [[ "$status" == "healthy" ]] && return 0
    sleep 2
  done
  echo "postgres did not become healthy in time" >&2
  exit 1
}

run_migrations() {
  echo "==> Running database migrations"
  "${BACKEND_COMPOSE[@]}" run --rm --no-deps --entrypoint /opt/venv/bin/python \
    clinic_care_service -m alembic upgrade head
}

start_backend() {
  echo "==> Starting backend service"
  "${BACKEND_COMPOSE[@]}" up -d --build
}

start_frontend() {
  echo "==> Starting frontend service"
  mkdir -p "$LOG_DIR"
  pushd "$ROOT_DIR/frontend" >/dev/null
  [[ -d node_modules ]] || npm install
  nohup npm run dev > "$FRONTEND_LOG" 2>&1 &
  echo $! > "$FRONTEND_PID_FILE"
  popd >/dev/null
  echo "Frontend started (pid $(cat "$FRONTEND_PID_FILE")), logs: $FRONTEND_LOG"
}

start_all() {
  ensure_network
  start_database
  wait_for_database
  run_migrations
  start_backend
  start_frontend
}

show_logs() {
  local service="${1:-}"
  shift || true
  case "$service" in
    db|database|postgres)
      "${DB_COMPOSE[@]}" logs "$@"
      ;;
    backend)
      "${BACKEND_COMPOSE[@]}" logs "$@"
      ;;
    frontend)
      if [[ ! -f "$FRONTEND_LOG" ]]; then
        echo "No frontend log yet. Start it first with: $0 up" >&2
        exit 1
      fi
      tail "$@" "$FRONTEND_LOG"
      ;;
    *)
      echo "Usage: $0 logs {db|backend|frontend} [-f]" >&2
      exit 1
      ;;
  esac
}

usage() {
  cat <<EOF
Usage: $0 [command]

Commands:
  up                     Start database, run migrations, then start backend and frontend (default)
  migrate                Run database migrations only
  logs <db|backend|frontend> [-f]   Tail logs for a service (-f to follow)
  help                   Show this help
EOF
}

command="${1:-up}"
shift || true

case "$command" in
  up)
    start_all
    ;;
  migrate)
    ensure_network
    run_migrations
    ;;
  logs)
    show_logs "$@"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage
    exit 1
    ;;
esac

