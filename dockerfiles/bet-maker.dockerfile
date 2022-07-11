FROM python:slim

ENV PYTHONPATH /bet-maker
ENV POETRY_VIRTUALENVS_CREATE false

RUN apt-get update && apt-get install -qq -y \
    build-essential libpq-dev netcat --no-install-recommends

WORKDIR /bet-maker/

RUN pip install --upgrade pip && pip install poetry psycopg2

COPY microservices/bet-maker/poetry.lock microservices/bet-maker/pyproject.toml /bet-maker/

RUN poetry install
COPY microservices/bet-maker/ /bet-maker/
COPY microservices/settings /bet-maker/microservices/settings