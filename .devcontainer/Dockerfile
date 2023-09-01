ARG build_for=linux/amd64
FROM --platform=$build_for python:3.11.2-slim-bullseye as base

RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
    git \
    ssh-client \
    software-properties-common \
    make \
    build-essential \
    ca-certificates \
    libpq-dev \
  && apt-get clean \
  && rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/*


WORKDIR /home/

COPY . .

RUN python -m pip install --upgrade pip