from dagster import asset
from sklearn.datasets import make_classification
import polars as pl
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")

@asset
def raw_data() -> str:
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)
    df = pl.DataFrame(X)
    df = df.with_columns(pl.Series(name="target", values=y))
    file_path = RAW_DATA_PATH / "raw_data.parquet"
    df.write_parquet(file_path)
    return str(file_path)
