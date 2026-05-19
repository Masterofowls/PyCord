# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=pycord.settings \
    PORT=8080

WORKDIR /app

# OS deps: build essentials, libpq for psycopg, curl for tailwind binary
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Build Tailwind + collect static at image build time
RUN python manage.py tailwind install --no-input || true && \
    python manage.py tailwind build --no-input || true && \
    SECRET_KEY=build DATABASE_URL=sqlite:///tmp.db \
      python manage.py collectstatic --noinput

EXPOSE 8080

# Daphne serves both HTTP + WebSocket via ASGI
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p ${PORT} pycord.asgi:application"]
