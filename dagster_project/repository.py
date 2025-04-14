from dagster import Definitions

from dagster_project.bronze_asset import bronze_asset
from dagster_project.silver_asset import silver_asset
from dagster_project.gold_asset import gold_asset

from dagster_project.jobs import bronze_to_silver_job, silver_to_gold_job

# Define the repository with assets and jobs
defs = Definitions(
    assets=[
        bronze_asset,
        silver_asset,
        gold_asset,
    ],
    jobs=[
        bronze_to_silver_job,
        silver_to_gold_job,
    ],
)
