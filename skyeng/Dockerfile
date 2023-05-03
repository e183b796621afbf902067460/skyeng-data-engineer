FROM python:3.10-slim

USER root
RUN apt-get update && apt-get install -y git

WORKDIR /opt/dagster/app
ENV DAGSTER_HOME=/opt/dagster/app

COPY requirements.txt .

COPY dagster.yaml ./
COPY workspace.yaml ./
COPY skyeng ./skyeng

RUN pip install -r requirements.txt
