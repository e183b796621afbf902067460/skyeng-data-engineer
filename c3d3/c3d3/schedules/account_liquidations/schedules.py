from dagster import ScheduleDefinition

from c3d3.jobs.account_liquidations.jobs import dag


every_minute = ScheduleDefinition(
    name='account_liquidations',
    job=dag,
    cron_schedule="*/1 * * * *"
)
