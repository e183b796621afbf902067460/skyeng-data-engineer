FROM apache/airflow:2.4.1

USER root

RUN apt-get update && apt-get install -y git

USER airflow

ENV ETH_HTTP_PROVIDER=""
ENV BSC_HTTP_PROVIDER=""
ENV AVAX_HTTP_PROVIDER=""
ENV ARB_HTTP_PROVIDER=""
ENV FTM_HTTP_PROVIDER=""
ENV MATIC_HTTP_PROVIDER=""
ENV OPT_HTTP_PROVIDER=""

RUN pip install -r requirements.txt

