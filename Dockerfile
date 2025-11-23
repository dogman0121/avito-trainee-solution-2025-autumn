FROM python:3.14-slim

ENV POETRY_VERSION=2.2.1

RUN pip install poetry==${POETRY_VERSION} gunicorn

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:create_app()"]