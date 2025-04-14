import pandas as pd
from dagster import asset, get_dagster_logger

@asset
def gold_asset(silver_asset: pd.DataFrame):
    logger = get_dagster_logger()

    logger.info("Starting transformation from silver to gold.")

    try:
        # Simple aggregation: sum value_times_two column
        df = silver_asset.copy()
        aggregation = df["value_times_two"].sum()

        # Create a new DataFrame with the aggregated result
        result_df = pd.DataFrame({
            "aggregation_type": ["sum"],
            "value_times_two_total": [aggregation]
        })

        logger.info(f"Aggregated data shape: {result_df.shape}")
        logger.info(f"Aggregated data preview:\n{result_df.to_string(index=False)}")

        # Define output file path
        output_file = "/data/gold/gold_data.csv"
        result_df.to_csv(output_file, index=False)
        logger.info(f"Gold data written to: {output_file}")

        return result_df

    except Exception as e:
        logger.error(f"Error processing gold data: {e}")
        raise
