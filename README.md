# DeFi Airflow
Depends on: [defi-head-core](https://github.com/e183b796621afbf902067460/defi-head-core), [defi-web3](https://github.com/e183b796621afbf902067460/defi-web3), [defi-traders-composite](https://github.com/e183b796621afbf902067460/defi-traders-composite), [defi-providers-fabric](https://github.com/e183b796621afbf902067460/defi-providers-fabric) and [defi-overviews-fabric](https://github.com/e183b796621afbf902067460/defi-overviews-fabric).

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
mkdir ./logs
```

- Put into `.env` permissions data:
```
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

- Set the __ENV__ variables in `docker-compose.yaml`:
  
  - Providers environment variables in [airflow-common-env](https://github.com/e183b796621afbf902067460/defi-airflow/blob/master/docker-compose.yaml#L50) service, by default:
 
    ```
    ETH_HTTP_PROVIDER: https://rpc.ankr.com/eth
    BSC_HTTP_PROVIDER: https://rpc.ankr.com/bsc
    AVAX_HTTP_PROVIDER: https://rpc.ankr.com/avalanche
    ARB_HTTP_PROVIDER: https://rpc.ankr.com/arbitrum
    FTM_HTTP_PROVIDER: https://rpc.ankr.com/fantom
    MATIC_HTTP_PROVIDER: https://rpc.ankr.com/polygon
    OPT_HTTP_PROVIDER: https://rpc.ankr.com/optimism
    ```

  - ClickHouse environment variables in [airflow-common-env]() service, by default:
    ```
    CLICKHOUSE_HOST: dwh
    CLICKHOUSE_DB: defi_management
    CLICKHOUSE_USER: defi_management
    CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
    CLICKHOUSE_PASSWORD: defi_management
    ```
  - PostgreSQL environment variables in [airflow-common-env](https://github.com/e183b796621afbf902067460/defi-airflow/blob/master/docker-compose.yaml#L50) service, by default:
    ```
    POSTGRES_HOST: orm
    POSTGRES_USER: defi_management
    POSTGRES_PASSWORD: defi_management
    POSTGRES_DB: defi_management
    ```
  - PostgreSQL connection ID in [airflow-common-env](https://github.com/e183b796621afbf902067460/defi-airflow/blob/master/docker-compose.yaml#L50) service, by default:
    ```
    AIRFLOW_CONN_POSTGRES_DEFI_MANAGEMENT: postgresql://defi_management:defi_management@orm/defi_management
    ```

# Docker

- Run docker commands (`sudo`):
```
docker build -t defi_airflow .
```

- Compose `airflow-init`:
```
docker-compose up airflow-init
```

- Run docker compose:
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
docker exec -it <CONTAINER ID> pytest orm/_fixtures/conftest.py
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
