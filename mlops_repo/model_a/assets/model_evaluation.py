from dagster import asset, AssetIn
import polars as pl
import pickle
from pathlib import Path
from sklearn.metrics import accuracy_score

EVALUATION_PATH = Path("data/evaluation")

@asset(ins={"processed_data": AssetIn(), "trained_model": AssetIn()})
def model_metrics(processed_data: str, trained_model: str) -> str:
    EVALUATION_PATH.mkdir(parents=True, exist_ok=True)
    df = pl.read_parquet(processed_data)
    X = df.drop("target").to_numpy()
    y = df["target"].to_numpy()
    with open(trained_model, "rb") as f:
        model = pickle.load(f)
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    metrics_path = EVALUATION_PATH / "metrics.txt"
    metrics_path.write_text(f"Accuracy: {acc:.4f}\n")
    return str(metrics_path)
