FROM python:3.10-slim-bullseye


ARG SPLEETER_VERSION=2.4.0
ENV MODEL_PATH=/model

RUN mkdir -p /model
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
RUN pip install musdb museval
RUN pip install spleeter==${SPLEETER_VERSION}

COPY app /app
WORKDIR /app

RUN pip install poetry
RUN poetry install

ENTRYPOINT ["poetry"]
CMD ["run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "src"]