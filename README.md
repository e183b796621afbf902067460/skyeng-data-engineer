# DeFi Airflow
Depends on: [defi-head-core](https://github.com/e183b796621afbf902067460/defi-head-core), [defi-web3](https://github.com/e183b796621afbf902067460/defi-web3), [defi-dwh-orm](https://github.com/e183b796621afbf902067460/defi-dwh-orm), [defi-traders-composite](https://github.com/e183b796621afbf902067460/defi-traders-composite), [defi-providers-fabric](https://github.com/e183b796621afbf902067460/defi-providers-fabric) and [defi-overviews-fabric](https://github.com/e183b796621afbf902067460/defi-overviews-fabric).

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
ENV ETH_HTTP_PROVIDER=""
ENV BSC_HTTP_PROVIDER=""
ENV AVAX_HTTP_PROVIDER=""
ENV ARB_HTTP_PROVIDER=""
ENV FTM_HTTP_PROVIDER=""
ENV MATIC_HTTP_PROVIDER=""
ENV OPT_HTTP_PROVIDER=""
```

- Set credentials in `docker-compose.yaml` and configure ports, by default:
```
DB_ADDRESS: orm
DB_USER: airflow
DB_PASSWORD: airflow
DB_NAME: dwh
```


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

# Fixtures

Additional fixtures can be added to check DAGs success rate.

- See existing containers:
```
docker ps
```

- Copy `airflow-worker's` \<CONTAINER ID> and run inside of it:
```
docker exec -it <CONTAINER ID> pytest fixtures/test_.py
```

# Exit
- To stop all running containers:
```
docker stop $(docker ps -a -q)
```
- And remove it all:
```
docker rm $(docker ps -a -q)
```
