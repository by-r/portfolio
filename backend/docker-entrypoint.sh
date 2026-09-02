#!/bin/sh
set -eu

echo "Applying database migrations..."
uv run --no-sync python manage.py migrate --noinput

echo "Collecting static files..."
uv run --no-sync python manage.py collectstatic --noinput

exec "$@"
