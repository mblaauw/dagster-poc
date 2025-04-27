from dagster import define_asset_job

gold_job = define_asset_job(name="gold_job", selection=["customer_order_summary"])
