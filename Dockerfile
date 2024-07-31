FROM ghcr.io/cfpb/regtech/sbl/python-alpine:3.12

ENV UVICORN_LOG_LEVEL=info

WORKDIR /usr/app

RUN pip install poetry

COPY --chown=sbl:sbl poetry.lock pyproject.toml alembic.ini ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY --chown=sbl:sbl ./src ./src
COPY --chown=sbl:sbl ./db_revisions ./db_revisions

WORKDIR /usr/app/src

EXPOSE 8888

USER sbl

CMD uvicorn regtech_user_fi_management.main:app --host 0.0.0.0 --port 8888 --log-config log-config.yml --log-level $UVICORN_LOG_LEVEL --timeout-keep-alive 65
