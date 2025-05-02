from dagster import asset, AssetIn
from sklearn.ensemble import RandomForestClassifier
import polars as pl
import pickle
from pathlib import Path

MODELS_PATH = Path("data/models")

@asset(ins={"processed_data": AssetIn()}, required_resource_keys={"model_registry"})
def trained_model(context, processed_data: str) -> str:
    MODELS_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.read_parquet(processed_data)
    X = df.drop("target").to_numpy()
    y = df["target"].to_numpy()
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    model_path = MODELS_PATH / "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    context.resources.model_registry.save_model(model_path)
    return str(model_path)
