from dagster import ScheduleDefinition

from c3d3.jobs.hedge_to_supplies.jobs import dag


every_minute = ScheduleDefinition(
    name='hedge_to_supplies',
    job=dag,
    cron_schedule="*/1 * * * *"
)
