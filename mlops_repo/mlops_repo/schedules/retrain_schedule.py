from dagster import ScheduleDefinition
from mlops_repo.jobs.mlops_job import mlops_job

retrain_schedule = ScheduleDefinition(
    job=mlops_job,
    cron_schedule="0 3 * * 1",
)
