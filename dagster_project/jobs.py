from dagster import job

from dagster_project.bronze_asset import bronze_asset
from dagster_project.silver_asset import silver_asset
from dagster_project.gold_asset import gold_asset

# Job: Process from Bronze to Silver
@job
def bronze_to_silver_job():
    silver_asset(bronze_asset())

# Job: Process from Silver to Gold
@job
def silver_to_gold_job():
    gold_asset(silver_asset())
