FROM python:3.10-slim-bullseye


ARG SPLEETER_VERSION=2.4.0
ENV MODEL_PATH=/model

RUN mkdir -p /model
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
RUN pip install musdb museval
RUN pip install spleeter==${SPLEETER_VERSION}
RUN pip install numpy==1.26.4

COPY app/pyproject.toml /app/pyproject.toml
COPY app/poetry.lock /app/poetry.lock
WORKDIR /app

RUN pip install poetry
RUN poetry install --no-root

RUN apt install unzip zip

COPY app /app

COPY tests /tests

RUN poetry add pytest