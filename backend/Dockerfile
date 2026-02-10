FROM python:3.12-slim

WORKDIR /app

# Instala dependências de sistema úteis para pacotes como psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Instala dependências Python básicas do backend
RUN pip install --no-cache-dir fastapi uvicorn[standard] psycopg2-binary

# Copia o código da aplicação
COPY ./app /app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Comando para subir a API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
