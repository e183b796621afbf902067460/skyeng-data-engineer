FROM apache/airflow:2.4.1

USER root

RUN apt-get update && apt-get install -y git

USER airflow

RUN pip install clickhouse-sqlalchemy
RUN pip install clickhouse-driver
RUN pip install passlib

RUN pip install git+https://github.com/e183b796621afbf902067460/defi-head-core.git#egg=defi-head-core
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-web3.git#egg=defi-web3
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-providers-fabric.git#egg=defi-providers-fabric
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-traders-composite.git#egg=defi-traders-composite
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-overviews-fabric.git#egg=defi-overviews-fabric
