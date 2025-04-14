import pandas as pd
from dagster import asset, get_dagster_logger

@asset
def silver_asset(bronze_asset: pd.DataFrame):
    logger = get_dagster_logger()

    logger.info("Starting transformation from bronze to silver.")

    try:
        # Simple transformation: add a calculated column
        df = bronze_asset.copy()
        df["value_times_two"] = df["value"] * 2

        logger.info(f"Transformed data shape: {df.shape}")
        logger.info(f"Transformed data preview:\n{df.head().to_string(index=False)}")

        # Define output file path
        output_file = "/data/silver/silver_data.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Silver data written to: {output_file}")

        return df

    except Exception as e:
        logger.error(f"Error processing silver data: {e}")
        raise
