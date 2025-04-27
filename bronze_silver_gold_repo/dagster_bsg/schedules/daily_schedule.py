from dagster import ScheduleDefinition
from dagster_bsg.jobs.gold_job import gold_job

daily_schedule = ScheduleDefinition(
    job=gold_job,
    cron_schedule="0 6 * * *",
)
