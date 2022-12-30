import pendulum

from airflow import DAG

from plugins.postgres.operators import PostgresWeb3ExecuteOperator
from plugins.web3.operators import Web3OverviewOperator
from plugins.clickhouse.operators import PandasDataFrameToClickHouseOperator

from dwh.cfg.engine import DWHSettings

import re

from dags.conf import conf


for protocolCategory, fabrics in conf.items():
    for overviewType, key in fabrics['fabrics'].items():
        dag_id: str = f'dynamic_generated_{re.sub("-", "_", key["fabricKey"])}_dag'

        with DAG(
            dag_id=dag_id,
            start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
            schedule_interval='*/10 * * * *',
            catchup=False,
            default_args={
                'retries': 1,
                'max_active_runs': 1
            }
        ) as dag:
            pools = PostgresWeb3ExecuteOperator(
                task_id=f'extract_{re.sub("-", "_", key["fabricKey"])}_task',
                postgres_conn_id='postgres_defi_management',
                sql='sql/select_all_pools.sql',
                params={
                    'overview_type': overviewType,
                    'protocol_category': protocolCategory.lower()
                },
                do_xcom_push=True,
                dag=dag
            )
            web3_overview = Web3OverviewOperator.override(
                task_id=f'web3_{re.sub("-", "_", key["fabricKey"])}_task'
            )(
                fabric_key=key['fabricKey'],
                rows=pools.output,
                overview_type=overviewType
            )
            PandasDataFrameToClickHouseOperator.override(
                task_id=f'pd_load_{re.sub("-", "_", key["fabricKey"])}_task'
            )(
                df=web3_overview,
                table='bigtable_defi_management',
                engine=DWHSettings.get_engine()
            )

            globals()[dag_id] = dag
