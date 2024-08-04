FROM python:3.10-slim-bullseye


ARG SPLEETER_VERSION=2.4.0
ENV MODEL_PATH=/model

RUN mkdir -p /model
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
RUN pip install musdb museval
RUN pip install spleeter==${SPLEETER_VERSION}
RUN pip install numpy==1.26.4