import pandas as pd
from dagster import asset, get_dagster_logger

@asset
def bronze_asset():
    logger = get_dagster_logger()

    # Define input file path
    input_file = "/data/bronze/bronze_data.csv"
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
