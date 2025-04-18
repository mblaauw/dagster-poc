from dagster import Definitions

from dagster_project.bronze_asset import bronze_asset
from dagster_project.silver_asset import silver_asset
from dagster_project.gold_asset import gold_asset
from dagster_project.resources import DataPaths

from dagster_project.jobs import bronze_to_silver_job, silver_to_gold_job, full_pipeline_job

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