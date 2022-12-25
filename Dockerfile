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

RUN pip install airflow-providers-clickhouse

RUN pip install git+https://github.com/e183b796621afbf902067460/defi-head-core.git#egg=defi-head-core
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-dwh-orm.git#egg=defi-dwh-orm
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-web3.git#egg=defi-web3
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-providers-fabric.git#egg=defi-providers-fabric
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-traders-composite.git#egg=defi-traders-composite
RUN pip install git+https://github.com/e183b796621afbf902067460/defi-overviews-fabric.git#egg=defi-overviews-fabric
