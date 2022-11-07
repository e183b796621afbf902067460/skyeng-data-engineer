import pendulum
import datetime
from airflow.decorators import dag

configs: dict = {
    'dex_pool_overview':
        {
            'protocolCategory': 'DEX'
        },
    'farming_pool_overview':
        {
            'protocolCategory': 'Farming'
        },
    'staking_pool_overview':
        {
            'protocolCategory': 'Staking'
        },
    'lending_pool_overview':
        {
            'protocolCategory': 'Lending'
        }
}

for dag_name, config in configs.items():
    dag_id: str = f'dynamic_generated_{dag_name}_dag'

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
        from tasks.getRowsForOverviews import getRowsForOverviews
        from tasks.getOverviews import getOverviews
        from tasks.loadOverviews import loadOverviews

        rows = getRowsForOverviews(protocolCategory=config['protocolCategory'])
        overviews = getOverviews(rows=rows, protocolCategory=config['protocolCategory'])
        loadOverviews(overviews=overviews, protocolCategory=config['protocolCategory'])

    globals()[dag_id] = dynamic_generated_dag()
