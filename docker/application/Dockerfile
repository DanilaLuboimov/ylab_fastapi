FROM python:3.10-slim

WORKDIR /fastapi_app

ENV PYTHONDONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY app .
