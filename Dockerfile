FROM python:3.10-slim as base
WORKDIR /usr/src/app
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y gcc libffi-dev g++

FROM node:16.13.0-alpine as client
WORKDIR /usr/src/app
COPY ./frontend /usr/src/app
RUN npm install --silent
RUN npm run build


FROM base as builder
WORKDIR /usr/src/app
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.14
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv
COPY ./backend/pyproject.toml ./backend/poetry.lock ./
RUN . /venv/bin/activate \
    && poetry install --no-dev --no-root \
    && playwright install chromium \
    && playwright install-deps

COPY ./backend .
RUN chmod +x docker-entrypoint.sh
COPY --from=client /usr/src/app/build/ /usr/src/app/src/bas_app/static/
RUN mv src/bas_app/static/static/* src/bas_app/static/
RUN rmdir src/bas_app/static/static
EXPOSE 5000
CMD ["./docker-entrypoint.sh"]