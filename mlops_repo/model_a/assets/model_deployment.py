from dagster import asset, AssetIn
from pathlib import Path
import shutil

@asset(ins={"trained_model": AssetIn()}, required_resource_keys={"model_registry"})
def deployed_model(context, trained_model: str) -> str:
    deployed_path = Path("data/models/deployed_model.pkl")
    shutil.copy(trained_model, deployed_path)
    context.log.info("Model deployed!")
    return str(deployed_path)
