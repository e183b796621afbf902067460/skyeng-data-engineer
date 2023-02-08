from dagster import ScheduleDefinition

from c3d3.jobs.account_limit_orders.jobs import dag


every_minute = ScheduleDefinition(
    name='account_limit_orders',
    job=dag,
    cron_schedule="*/1 * * * *"
)
