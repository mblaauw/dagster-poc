from dagster import asset, AssetIn
import polars as pl
from pathlib import Path

SILVER_PATH = Path("data/silver")

@asset(ins={"customers_bronze": AssetIn()}, required_resource_keys={"duckdb"})
def customers_silver(context, customers_bronze: str) -> str:
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.read_parquet(customers_bronze)
    df = df.with_columns((pl.col("age") + 1).alias("age"))
    file_path = SILVER_PATH / "customers_clean.parquet"
    df.write_parquet(file_path)
    context.log.info(f"Saved {file_path}")
    return str(file_path)

@asset(ins={"orders_bronze": AssetIn()}, required_resource_keys={"duckdb"})
def orders_silver(context, orders_bronze: str) -> str:
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.read_parquet(orders_bronze)
    file_path = SILVER_PATH / "orders_clean.parquet"
    df.write_parquet(file_path)
    context.log.info(f"Saved {file_path}")
    return str(file_path)
