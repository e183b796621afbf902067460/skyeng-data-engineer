import pendulum
import datetime
from airflow.decorators import dag

configs: dict = {
    'liquidity_pool_overview': {'overviewType': 'liquidity-pool-overview'},
    'staking_pool_overview': {'overviewType': 'staking-pool-overview'},
    'lending_pool_overview': {'overviewType': 'lending-pool-overview'}
}

for config_name, config in configs.items():
    dag_id: str = f'dynamic_generated_{config_name}_dag'

    @dag(
        dag_id=dag_id,
        start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
        schedule_interval='*/5 * * * *',
        catchup=False,
        default_args={
            'retries': 1,
            'execution_timeout': datetime.timedelta(minutes=5),
            'retry_delay': datetime.timedelta(seconds=30),
            'max_active_runs': 1
        }
    )
    def dynamic_generated_dag():
        from funcs.poolOverviews.getRows.task import getRows
        from funcs.poolOverviews.getOverviews.task import getOverviews
        from funcs.poolOverviews.loadOverviews.task import loadOverviews

        rows = getRows(overviewType=config['overviewType'])
        overviews = getOverviews(rows=rows, overviewType=config['overviewType'])
        loadOverviews(overviews=overviews, overviewType=config['overviewType'])

    globals()[dag_id] = dynamic_generated_dag()
