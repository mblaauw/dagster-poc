import os
import pandas as pd
from dagster import asset, get_dagster_logger
from dagster_repo.data_generator import generate_gold_data

@asset(required_resource_keys={"data_paths"})
def gold_asset(context, silver_asset: pd.DataFrame):
    logger = get_dagster_logger()

    logger.info("Starting transformation from silver to gold.")

    try:
        # Define output file path using resource
        gold_path = context.resources.data_paths.gold_path
        output_file = f"{gold_path}gold_data.csv"

        # Check if file exists, if not generate it
        if not os.path.exists(output_file):
            logger.info(f"Gold data file not found at {output_file}. Generating dummy data...")
            result_df = generate_gold_data(output_file)
        else:
            # Simple aggregation: sum value_times_two column
            df = silver_asset.copy()
            aggregation = df["value_times_two"].sum()

            # Create a new DataFrame with the aggregated result
            result_df = pd.DataFrame({
                "aggregation_type": ["sum"],
                "value_times_two_total": [aggregation]
            })

            result_df.to_csv(output_file, index=False)
            logger.info(f"Gold data written to: {output_file}")

        logger.info(f"Aggregated data shape: {result_df.shape}")
        logger.info(f"Aggregated data preview:\n{result_df.to_string(index=False)}")

        return result_df

    except Exception as e:
        logger.error(f"Error processing gold data: {e}")
        raise