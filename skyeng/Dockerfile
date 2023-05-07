FROM apache/airflow:2.3.0

USER root
RUN apt-get update && apt-get install -y git

USER airflow

ADD requirements.txt .
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt