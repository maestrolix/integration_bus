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

uvicorn ssd_fastapi.composites.http_api:app --port 5002 --host 0.0.0.0
