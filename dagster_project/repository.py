from dagster import Definitions

from dagster_repo.bronze_asset import bronze_asset
from dagster_repo.silver_asset import silver_asset
from dagster_repo.gold_asset import gold_asset
from dagster_repo.resources import DataPaths

from dagster_repo.jobs import bronze_to_silver_job, silver_to_gold_job, full_pipeline_job

# Define the repository with assets, jobs, and resources
defs = Definitions(
    assets=[
        bronze_asset,
        silver_asset,
        gold_asset,
    ],
    jobs=[
        bronze_to_silver_job,
        silver_to_gold_job,
        full_pipeline_job,
    ],
    resources={
        "data_paths": DataPaths(),
    }
)