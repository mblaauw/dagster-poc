from dotenv import load_dotenv
load_dotenv()

import os
from dagster import Definitions

from bvi_pipeline.jobs import bvi_job
from bvi_pipeline.schedules import bvi_schedule
from bvi_pipeline.sensors import bvi_sensor
from bvi_pipeline.assets import bvi_assets


# Try to import Postgres resource (only needed in prod)
try:
    from bvi_pipeline.resources import postgres_resource
except ImportError:
    postgres_resource = None

# Configure resources if Postgres env vars are set
resources_config = {}

if os.getenv("DAGSTER_PG_USERNAME"):
    resources_config["postgres"] = postgres_resource.configured({
        "username": os.getenv("DAGSTER_PG_USERNAME"),
        "password": os.getenv("DAGSTER_PG_PASSWORD"),
        "hostname": os.getenv("DAGSTER_PG_HOSTNAME"),
        "db_name": os.getenv("DAGSTER_PG_DB_NAME"),
        "port": int(os.getenv("DAGSTER_PG_PORT")),
    })

defs = Definitions(
    jobs=[bvi_job],
    schedules=[bvi_schedule],
    sensors=[bvi_sensor],
    assets=[*bvi_assets],
    resources=resources_config,
)