FROM us-central1-docker.pkg.dev/taranis-api/base-images/ubuntu20.04-python3.8-datascience

RUN mkdir -p /app
WORKDIR /app
COPY . /app
