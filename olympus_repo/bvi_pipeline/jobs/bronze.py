from dagster import define_asset_job, AssetSelection

# Bronze layer job - Raw data ingestion
bronze_job = define_asset_job(
    name="bronze_job",
    selection=AssetSelection.groups("bronze"),
    description="Job to ingest raw data into bronze layer"
)