from dagster import ScheduleDefinition
from .jobs import bvi_job

bvi_schedule = ScheduleDefinition(
    job=bvi_job,
    cron_schedule="0 * * * *",  # every hour
)