from dagster import job

from dagster_repo.bronze_asset import bronze_asset
from dagster_repo.silver_asset import silver_asset
from dagster_repo.gold_asset import gold_asset

# Job: Process from Bronze to Silver
@job
def bronze_to_silver_job():
    silver_asset(bronze_asset())

# Job: Process from Silver to Gold
@job
def silver_to_gold_job():
    gold_asset(silver_asset())

# Job: Complete pipeline from Bronze to Gold
@job
def full_pipeline_job():
    # This job runs the entire pipeline
    gold_asset(silver_asset(bronze_asset()))