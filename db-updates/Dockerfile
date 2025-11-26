FROM ghcr.io/astral-sh/uv:debian-slim

COPY . /code/db-updates

WORKDIR /code/db-updates

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN uv sync --locked

CMD ["uv", "run", "-m", "src.main"]