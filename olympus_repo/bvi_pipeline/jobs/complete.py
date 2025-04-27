from dagster import define_asset_job, AssetSelection

# Complete pipeline job - Run all layers
bvi_job = define_asset_job(
    name="bvi_job",
    selection=AssetSelection.groups("bronze", "silver", "gold"),
    description="Complete BVI pipeline job running all layers"
)