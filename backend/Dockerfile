FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN groupadd -r appuser && \
    useradd -r -g appuser -d /home/appuser -s /usr/sbin/nologin -m appuser

ENV HOME=/home/appuser

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    unzip \
    libpq5 \
    libmagic1 \
    zlib1g-dev

COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /usr/local/bin/uv

# Dependency layer
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-dev \
    --no-install-project

# Application layer
COPY --chown=appuser:appuser . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-dev && \
    find . -type d -name __pycache__ -exec rm -rf {} + && \
    chmod +x /app/docker-entrypoint.sh && \
    chown -R appuser:appuser /app /opt/venv ${HOME}

EXPOSE 8090

USER appuser

ENTRYPOINT ["/app/docker-entrypoint.sh"]
