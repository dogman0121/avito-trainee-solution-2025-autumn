FROM python:3.13-slim-bullseye

ENV POETRY_VERSION=2.2.1

RUN pip install poetry==${POETRY_VERSION} gunicorn

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

RUN chmod a+x boot.sh

EXPOSE 8080

ENTRYPOINT ["./boot.sh"]