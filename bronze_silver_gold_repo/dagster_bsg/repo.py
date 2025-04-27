# dagster_bsg/repo.py
from dagster import Definitions, load_assets_from_modules

from dagster_bsg.assets import bronze_assets, silver_assets, gold_assets
from dagster_bsg.jobs.bronze_job import bronze_job
from dagster_bsg.jobs.silver_job import silver_job
from dagster_bsg.jobs.gold_job import gold_job
from dagster_bsg.resources.duckdb_resource import duckdb_resource
from dagster_bsg.schedules.daily_schedule import daily_schedule

all_assets = load_assets_from_modules([bronze_assets, silver_assets, gold_assets])

defs = Definitions(
    assets=all_assets,
    jobs=[bronze_job, silver_job, gold_job],
    resources={"duckdb": duckdb_resource},
    schedules=[daily_schedule],
)
