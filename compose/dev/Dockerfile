# Alias for the specific Python version
FROM python:3.12.4-slim-bookworm as python

# Build stage
FROM python as build-stage

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && \
  apt-get install --no-install-recommends -y gcc

COPY ./requirements.dev.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.dev.txt

# Run stage
FROM python as run-stage

WORKDIR /app

EXPOSE 8000

COPY --from=build-stage /app/wheels /wheels
COPY --from=build-stage /app/requirements.dev.txt .
COPY . .

RUN pip install --no-cache-dir /wheels/*

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
