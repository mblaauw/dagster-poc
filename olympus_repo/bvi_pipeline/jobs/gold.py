from dagster import define_asset_job, AssetSelection

# Gold layer job - Business-ready data
gold_job = define_asset_job(
    name="gold_job",
    selection=AssetSelection.groups("gold"),
    description="Job to create business-ready data in gold layer"
)