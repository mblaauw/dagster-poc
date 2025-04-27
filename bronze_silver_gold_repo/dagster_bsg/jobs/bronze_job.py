from dagster import define_asset_job

bronze_job = define_asset_job(name="bronze_job", selection=["customers_bronze", "orders_bronze"])
