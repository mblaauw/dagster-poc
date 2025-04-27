from dagster import define_asset_job, AssetSelection

# Bronze layer job - Raw data ingestion
bronze_job = define_asset_job(
    name="bronze_job",
    selection=AssetSelection.groups("bronze"),
    description="Job to ingest raw data into bronze layer"
)

# Silver layer job - Data cleaning and standardization
silver_job = define_asset_job(
    name="silver_job",
    selection=AssetSelection.groups("silver"),
    description="Job to clean and standardize data in silver layer"
)

# Gold layer job - Business-ready data
gold_job = define_asset_job(
    name="gold_job",
    selection=AssetSelection.groups("gold"),
    description="Job to create business-ready data in gold layer"
)

# Complete pipeline job - Run all layers
bvi_job = define_asset_job(
    name="bvi_job",
    selection=AssetSelection.groups("bronze", "silver", "gold"),
    description="Complete BVI pipeline job running all layers"
)