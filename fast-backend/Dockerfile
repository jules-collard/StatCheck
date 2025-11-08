FROM ghcr.io/astral-sh/uv:debian-slim

COPY . /code/backend

WORKDIR /code/backend

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN uv sync --locked

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "80"]