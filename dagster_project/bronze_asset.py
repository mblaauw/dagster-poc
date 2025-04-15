import pandas as pd
from dagster import asset, get_dagster_logger
from dagster_project.resources import DataPaths

@asset(required_resource_keys={"data_paths"})
def bronze_asset(context):
    logger = get_dagster_logger()

    # Use resource for path
    bronze_path = context.resources.data_paths.bronze_path
    input_file = f"{bronze_path}bronze_data.csv"
    logger.info(f"Reading bronze data from: {input_file}")

    try:
        # Read CSV into DataFrame
        df = pd.read_csv(input_file)

        # Log basic DataFrame info
        logger.info(f"Bronze data shape: {df.shape}")
        logger.info(f"Bronze data preview:\n{df.head().to_string(index=False)}")

        return df

    except Exception as e:
        logger.error(f"Error reading bronze data: {e}")
        raise