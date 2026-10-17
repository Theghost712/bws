#!/usr/bin/env bash
# Vercel build step: apply database migrations before the app is deployed.
# Vercel still runs collectstatic automatically for Django projects.
set -e

if [ -n "$DATABASE_URL" ] || [ -n "$POSTGRES_URL" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
else
    echo "No DATABASE_URL/POSTGRES_URL configured; skipping migrations."
fi
