from dagster import Definitions, load_assets_from_modules
from mlops_repo.assets import data_ingestion, data_preprocessing, model_training, model_evaluation, model_deployment
from mlops_repo.jobs.mlops_job import mlops_job
from mlops_repo.resources.model_registry import model_registry
from mlops_repo.schedules.retrain_schedule import retrain_schedule

all_assets = load_assets_from_modules([
    data_ingestion,
    data_preprocessing,
    model_training,
    model_evaluation,
    model_deployment,
])

defs = Definitions(
    assets=all_assets,
    jobs=[mlops_job],
    resources={"model_registry": model_registry},
    schedules=[retrain_schedule]
)
