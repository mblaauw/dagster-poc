from dagster import asset, AssetIn
import polars as pl
from pathlib import Path

GOLD_PATH = Path("data/gold")

@asset(ins={"customers_silver": AssetIn(), "orders_silver": AssetIn()}, required_resource_keys={"duckdb"})
def customer_order_summary(context, customers_silver: str, orders_silver: str) -> str:
    GOLD_PATH.mkdir(parents=True, exist_ok=True)
    customers = pl.read_parquet(customers_silver)
    orders = pl.read_parquet(orders_silver)
    summary = orders.join(customers, on="customer_id").group_by("name").agg(pl.sum("amount"))
    file_path = GOLD_PATH / "customer_order_summary.parquet"
    summary.write_parquet(file_path)
    context.log.info(f"Saved {file_path}")
    return str(file_path)
