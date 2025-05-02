from dagster import asset, AssetIn
from sklearn.preprocessing import StandardScaler
import polars as pl
import pickle
from pathlib import Path

PROCESSED_DATA_PATH = Path("data/processed")

@asset(ins={"raw_data": AssetIn()})
def processed_data(raw_data: str) -> str:
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.read_parquet(raw_data)
    features = df.drop("target").to_numpy()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    df_proc = pl.DataFrame(scaled_features)
    df_proc = df_proc.with_columns(pl.Series(name="target", values=df["target"]))
    file_path = PROCESSED_DATA_PATH / "processed_data.parquet"
    df_proc.write_parquet(file_path)

    with open(PROCESSED_DATA_PATH / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    return str(file_path)
