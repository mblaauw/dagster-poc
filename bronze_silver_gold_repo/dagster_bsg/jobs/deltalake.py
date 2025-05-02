from dagster import job
from ..ops import write_sample_data_to_delta, read_from_delta


@job
def delta_job():
    read_from_delta(write_sample_data_to_delta())
