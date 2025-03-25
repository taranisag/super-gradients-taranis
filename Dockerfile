FROM python:3.10

RUN mkdir -p /app
WORKDIR /app
COPY . /app
