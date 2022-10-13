FROM apache/airflow:2.4.1

USER airflow

ENV DB_ADDRESS=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_NAME=""

ENV ETH_HTTP_PROVIDER=""
ENV BSC_HTTP_PROVIDER=""
ENV AVAX_HTTP_PROVIDER=""
ENV ARB_HTTP_PROVIDER=""
ENV FTM_HTTP_PROVIDER=""
ENV MATIC_HTTP_PROVIDER=""
ENV OPT_HTTP_PROVIDER=""

RUN pip3 install git+https://github.com/e183b796621afbf902067460/defi-head-core.git
RUN pip3 install git+https://github.com/e183b796621afbf902067460/defi-contracts-evm.git
RUN pip3 install git+https://github.com/e183b796621afbf902067460/defi-dwh-orm.git
RUN pip3 install git+https://github.com/e183b796621afbf902067460/defi-providers-fabric.git
RUN pip3 install git+https://github.com/e183b796621afbf902067460/defi-traders-composite.git
RUN pip3 install git+https://github.com/e183b796621afbf902067460/defi-overviews-fabric.git

RUN pip3 install apache-airflow
