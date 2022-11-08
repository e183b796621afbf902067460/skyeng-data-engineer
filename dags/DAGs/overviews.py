import pendulum
import datetime
from airflow.decorators import dag
import re


configs: dict = {
    'DEX': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'dex-pool-allocation-overview'
            },
            'pool': {
                'fabricKey': 'dex-pool-overview'
            }
        }
    },
    'Farming': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'farming-pool-allocation-overview'
            },
            'incentive': {
                'fabricKey': 'farming-pool-incentive-overview'
            },
            'pool': {
                'fabricKey': 'farming-pool-overview'
            }
        }
    },
    'Staking': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'staking-pool-allocation-overview'
            },
            'incentive': {
                'fabricKey': 'staking-pool-incentive-overview'
            },
            'pool': {
                'fabricKey': 'staking-pool-overview'
            }
        }
    },
    'Lending': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'lending-pool-allocation-overview'
            },
            'borrow': {
                'fabricKey': 'lending-pool-borrow-overview'
            },
            'incentive': {
                'fabricKey': 'lending-pool-incentive-overview'
            },
            'pool': {
                'fabricKey': 'lending-pool-overview'
            }
        }
    }
}

for protocolCategory, fabrics in configs.items():
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
            from tasks.getRowsForOverviews import getRowsForOverviews
            from tasks.getOverviews import getOverviews
            from tasks.loadOverviews import loadOverviews

            rows = getRowsForOverviews(protocolCategory=protocolCategory, overviewType=overviewType)
            overviews = getOverviews(rows=rows, fabricKey=key['fabricKey'], overviewType=overviewType)
            loadOverviews(overviews=overviews, protocolCategory=protocolCategory, overviewType=overviewType, fabricKey=key['fabricKey'])

        globals()[dag_id] = dynamic_generated_dag()
