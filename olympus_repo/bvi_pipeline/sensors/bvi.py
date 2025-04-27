from dagster import RunRequest, sensor
from ..jobs import bvi_job

@sensor(job=bvi_job)
def bvi_sensor(context):
    if context.last_completion_time is None:
        yield RunRequest(run_key=None, run_config={})