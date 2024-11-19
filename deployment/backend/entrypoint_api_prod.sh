#!/usr/bin/env bash
set -e
if [ -z "$API_LOG_LEVEL" ]; then
  API_LOG_LEVEL=info
fi
if [ -z "$API_PORT" ]; then
  API_PORT=5002
fi

entrypoint_await.sh
entrypoint_migrations.sh

CORE_COUNT=$(nproc)
echo $CORE_COUNT

gunicorn ssd_fastapi.composites.http_api:app --workers $CORE_COUNT --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5002
