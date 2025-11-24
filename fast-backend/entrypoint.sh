#!/bin/sh

uv run alembic upgrade head
uv run fastapi run app/main.py --port 80