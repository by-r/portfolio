FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

RUN pip install --no-cache-dir uv

# Development image: installs dev dependencies; source is bind-mounted by Compose.
FROM base AS development

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen

# Production image: only production dependencies and application code.
FROM base AS production

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev

COPY backend/ ./
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60"]
