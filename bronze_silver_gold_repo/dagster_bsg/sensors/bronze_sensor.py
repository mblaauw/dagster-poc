from dagster import sensor, RunRequest
from dagster_bsg.jobs.bronze_job import bronze_job

@sensor(job=bronze_job)
def bronze_sensor():
    yield RunRequest(run_key=None, run_config={})
