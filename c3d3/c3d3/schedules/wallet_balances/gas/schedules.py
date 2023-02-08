from dagster import ScheduleDefinition

from c3d3.jobs.wallet_balances.gas.jobs import dag


every_minute = ScheduleDefinition(
    name='wallet_balances_gas',
    job=dag,
    cron_schedule="*/1 * * * *"
)
