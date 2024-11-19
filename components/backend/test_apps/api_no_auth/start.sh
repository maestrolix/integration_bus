#!/usr/bin/env bash
sleep 5
alembic upgrade head && python3 ./start.py
