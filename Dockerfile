FROM python:3.10

RUN pip install requests

RUN mkdir -p /app
WORKDIR /app
COPY . /app
