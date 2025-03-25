FROM python:3.10

RUN PIP install requests

RUN mkdir -p /app
WORKDIR /app
COPY . /app
