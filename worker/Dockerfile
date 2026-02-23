FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    build-essential

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

# evita venv dentro do container
RUN poetry config virtualenvs.create false

# instala deps principais primeiro (mais estável)
RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY worker/. .

CMD ["python", "worker.py"]
