FROM python:3.11-alpine

WORKDIR /usr/app

RUN pip install poetry

COPY poetry.lock pyproject.toml alembic.ini ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./src ./src
COPY ./db_revisions ./db_revisions

WORKDIR /usr/app/src

EXPOSE 8888

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]