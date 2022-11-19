import pendulum
import datetime
from airflow.decorators import dag
import re

from dags.conf import conf, exposureTypes


for protocolCategory, fabrics in conf.items():
    for overviewType, key in fabrics['fabrics'].items():
        dag_id: str = f'dynamic_generated_{re.sub("-", "_", key["fabricKey"])}_dag'

        @dag(
            dag_id=dag_id,
            start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
            schedule_interval='*/10 * * * *',
            catchup=False,
            default_args={
                'retries': 1,
                'execution_timeout': datetime.timedelta(minutes=10),
                'retry_delay': datetime.timedelta(seconds=30),
                'max_active_runs': 1
            }
        )
        def dynamic_generated_dag():
            from src.tasks.extractRowsForOverviews import extractRowsForOverviews
            from src.tasks.getOverviews import getOverviews
            from src.tasks.loadOverviews import loadOverviews

            rows = extractRowsForOverviews(
                protocolCategory=protocolCategory,
                overviewType=overviewType,
                exposureTypes=exposureTypes
            )
            overviews = getOverviews(
                rows=rows,
                fabricKey=key['fabricKey'],
                overviewType=overviewType,
                exposureTypes=exposureTypes
            )
            loadOverviews(
                overviews=overviews,
                protocolCategory=protocolCategory,
                overviewType=overviewType,
                fabricKey=key['fabricKey']
            )

        globals()[dag_id] = dynamic_generated_dag()
