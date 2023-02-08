from dagster import ScheduleDefinition

from c3d3.jobs.account_balances.jobs import dag


every_minute = ScheduleDefinition(
    name='account_balances',
    job=dag,
    cron_schedule="*/1 * * * *"
)
