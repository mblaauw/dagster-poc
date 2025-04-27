import os
import pandas as pd
from dagster import asset, get_dagster_logger
from dagster_repo.data_generator import generate_bronze_data

@asset(required_resource_keys={"data_paths"})
def bronze_asset(context):
    logger = get_dagster_logger()

    # Use resource for path
    bronze_path = context.resources.data_paths.bronze_path
    input_file = f"{bronze_path}bronze_data.csv"
    logger.info(f"Reading bronze data from: {input_file}")

    try:
        # Check if file exists, if not generate it
        if not os.path.exists(input_file):
            logger.info(f"Bronze data file not found at {input_file}. Generating dummy data...")
            df = generate_bronze_data(input_file)
        else:
            # Read CSV into DataFrame
            df = pd.read_csv(input_file)

        # Log basic DataFrame info
        logger.info(f"Bronze data shape: {df.shape}")
        logger.info(f"Bronze data preview:\n{df.head().to_string(index=False)}")

        return df

    except Exception as e:
        logger.error(f"Error reading bronze data: {e}")
        raise