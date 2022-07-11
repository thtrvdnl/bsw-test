FROM python:slim

ENV PYTHONPATH /line-provider
ENV POETRY_VIRTUALENVS_CREATE false

RUN apt-get update && apt-get install -qq -y \
    build-essential libpq-dev netcat --no-install-recommends

WORKDIR /line-provider/

RUN pip install --upgrade pip && pip install poetry psycopg2

COPY microservices/line-provider/poetry.lock microservices/line-provider/pyproject.toml /line-provider/

RUN poetry install
COPY microservices/line-provider/ /line-provider/
COPY microservices/settings/ /line-provider/microservices/settings