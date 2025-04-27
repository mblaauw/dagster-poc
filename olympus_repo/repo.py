import os
from dotenv import load_dotenv
from dagster import Definitions

from bvi_pipeline.jobs import bvi_jobs
from bvi_pipeline.schedules import bvi_schedules
from bvi_pipeline.sensors import bvi_sensors
from bvi_pipeline.assets import bvi_assets
from bvi_pipeline.ops import bvi_ops
from bvi_pipeline.resources import db_connection

load_dotenv()

# Configure resources
resources_config = {}

if os.getenv("DAGSTER_PG_USERNAME"):
    resources_config["db_connection"] = db_connection.configured({
        "username": os.getenv("DAGSTER_PG_USERNAME"),
        "password": os.getenv("DAGSTER_PG_PASSWORD"),
        "hostname": os.getenv("DAGSTER_PG_HOSTNAME"),
        "db_name": os.getenv("DAGSTER_PG_DB_NAME"),
        "port": int(os.getenv("DAGSTER_PG_PORT")),
    })

defs = Definitions(
    jobs=bvi_jobs,
    schedules=bvi_schedules,
    sensors=bvi_sensors,
    assets=bvi_assets,
    ops=bvi_ops,
    resources=resources_config,
)