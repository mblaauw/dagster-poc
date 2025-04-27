import os
import pandas as pd
from dagster import asset, get_dagster_logger
from dagster_repo.data_generator import generate_silver_data

@asset(required_resource_keys={"data_paths"})
def silver_asset(context, bronze_asset: pd.DataFrame):
    logger = get_dagster_logger()

    logger.info("Starting transformation from bronze to silver.")

    try:
        # Define output file path using resource
        silver_path = context.resources.data_paths.silver_path
        output_file = f"{silver_path}silver_data.csv"

        # Check if file exists, if not generate it
        if not os.path.exists(output_file):
            logger.info(f"Silver data file not found at {output_file}. Generating dummy data...")
            df = generate_silver_data(output_file)
        else:
            # Simple transformation: add a calculated column
            df = bronze_asset.copy()
            df["value_times_two"] = df["value"] * 2
            df.to_csv(output_file, index=False)
            logger.info(f"Silver data written to: {output_file}")

        logger.info(f"Transformed data shape: {df.shape}")
        logger.info(f"Transformed data preview:\n{df.head().to_string(index=False)}")

        return df

    except Exception as e:
        logger.error(f"Error processing silver data: {e}")
        raise