from dagster import define_asset_job, AssetSelection

# Silver layer job - Data cleaning and standardization
silver_job = define_asset_job(
    name="silver_job",
    selection=AssetSelection.groups("silver"),
    description="Job to clean and standardize data in silver layer"
)