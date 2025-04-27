from dagster import define_asset_job

silver_job = define_asset_job(name="silver_job", selection=["customers_silver", "orders_silver"])
