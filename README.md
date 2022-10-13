# DeFi Airflow
Depends on: [defi-head-core](https://github.com/e183b796621afbf902067460/defi-head-core), [defi-contracts-evm](https://github.com/e183b796621afbf902067460/defi-contracts-evm), [defi-dwh-orm](https://github.com/e183b796621afbf902067460/defi-dwh-orm), [defi-traders-composite](https://github.com/e183b796621afbf902067460/defi-traders-composite), [defi-providers-fabric](https://github.com/e183b796621afbf902067460/defi-providers-fabric) and [defi-overviews-fabric](https://github.com/e183b796621afbf902067460/defi-overviews-fabric).

---

Apache Airflow is used for DeFi ETL orchestration.

# Configuration

First of all to configure an Airflow Worker correctly need to do next steps:

- Clone current repository:
```
git clone https://github.com/e183b796621afbf902067460/defi-airflow.git
```

- Get into the project folder:
```
cd defi-airflow/
```

- Create requirement folders:
```
mkdir ./logs ./plugins
```

- Put into `.env` permissions data:
```
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

- Set the __ENV__ variables in `Dockerfile`:
```
ENV DB_ADDRESS=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_NAME=""
```
```
ENV ETH_HTTP_PROVIDER=""
ENV BSC_HTTP_PROVIDER=""
ENV AVAX_HTTP_PROVIDER=""
ENV ARB_HTTP_PROVIDER=""
ENV FTM_HTTP_PROVIDER=""
ENV MATIC_HTTP_PROVIDER=""
ENV OPT_HTTP_PROVIDER=""
```

- Set credentials in `docker-compose.yaml` and configure ports.

# Docker

- Run docker commands (`sudo`):
```
docker build -t defi_airflow .
```

- Compose:
```
docker-compose up airflow-init
```

- Then:
```
docker-compose up -d
```
---
Afer running those command we can check existing containers by typing:
```
docker ps
```
