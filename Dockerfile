FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry install

RUN pip install gunicorn

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]