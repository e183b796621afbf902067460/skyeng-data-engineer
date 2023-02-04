from dagster import ScheduleDefinition

from c3d3.jobs.wallet_balances.erc20.jobs import dag


every_10th_minute = ScheduleDefinition(job=dag, cron_schedule="*/1 * * * *")
