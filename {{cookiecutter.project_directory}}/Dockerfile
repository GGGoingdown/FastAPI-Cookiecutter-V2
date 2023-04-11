FROM python:3.9-slim as requirements-stage
WORKDIR /tmp
ARG ENVIRONMENT=PROD
RUN pip install --upgrade pip poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN if [ "$ENVIRONMENT" = "PROD" ] || [ "$ENVIRONMENT" = "STAG" ] ; then poetry export -f requirements.txt --output requirements.txt --without-hashes ; else poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev; fi

FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

WORKDIR /app
#TODO: Use this for postgresql
# RUN apt-get update && apt-get install -y libpq-dev gcc

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Application src
COPY ./app /app/app

#TODO: Application pre-start script
# COPY ./pre_start /app/pre_start

# DB Migration
# COPY ./migrations /app/migrations

# Script
COPY ./script /app/script

# Pyproject
COPY pyproject.toml .

RUN chmod +x /app/script/entrypoint.sh

EXPOSE 8000
