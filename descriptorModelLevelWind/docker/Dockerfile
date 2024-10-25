FROM ubuntu:22.04 as base

COPY ./scripts/* /scripts/
COPY ./requirements.txt /scripts/

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=true

SHELL ["/bin/bash", "-e"]
RUN /scripts/setup.sh
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"