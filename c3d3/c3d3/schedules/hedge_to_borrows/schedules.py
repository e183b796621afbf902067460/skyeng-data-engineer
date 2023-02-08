from dagster import ScheduleDefinition

from c3d3.jobs.hedge_to_borrows.jobs import dag


every_minute = ScheduleDefinition(
    name='hedge_to_borrows',
    job=dag,
    cron_schedule="*/1 * * * *"
)
