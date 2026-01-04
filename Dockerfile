FROM python:3.13-bullseye

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VERSION=1.8.1

WORKDIR /code

RUN \
  apt-get update \
  && apt-get -y install net-tools iputils-ping iproute2 gettext \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir poetry=="$POETRY_VERSION" \
  && apt-get clean

COPY ./src/pyproject.toml .
COPY ./src/poetry.lock .

RUN poetry install

COPY ./src .

EXPOSE 8000