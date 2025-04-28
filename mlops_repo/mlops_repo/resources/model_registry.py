from dagster import resource
from pathlib import Path

@resource
def model_registry():
    class Registry:
        def save_model(self, path: Path):
            print(f"[Registry] Model saved: {path}")
    return Registry()
