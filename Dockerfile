FROM python:3.12-alpine AS builder

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache-dir uv && \
    uv export --no-hashes --no-dev --format requirements-txt > requirements.prod.txt

FROM python:3.12-alpine AS dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder requirements.prod.txt /app

RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache-dir -r requirements.dev.txt

COPY . .
