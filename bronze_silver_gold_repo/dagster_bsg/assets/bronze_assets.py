from dagster import asset
import polars as pl
from pathlib import Path

BRONZE_PATH = Path("data/bronze")

@asset
def customers_bronze() -> str:
    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.DataFrame({
        "customer_id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    file_path = BRONZE_PATH / "customers.parquet"
    df.write_parquet(file_path)
    return str(file_path)

@asset
def orders_bronze() -> str:
    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.DataFrame({
        "order_id": [100, 101, 102],
        "customer_id": [1, 2, 3],
        "amount": [250.5, 150.0, 320.0]
    })
    file_path = BRONZE_PATH / "orders.parquet"
    df.write_parquet(file_path)
    return str(file_path)
