import os
import pandas as pd
import numpy as np
from dagster import get_dagster_logger

def generate_bronze_data(output_path):
    """Generate dummy bronze data and save it to the specified path."""
    logger = get_dagster_logger()

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate dummy data
    data = {
        'id': range(1, 11),
        'name': [f'item_{i}' for i in range(1, 11)],
        'value': np.random.randint(100, 1000, 10)
    }

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Generated bronze data with {len(df)} rows and saved to {output_path}")

    return df

def generate_silver_data(output_path):
    """Generate dummy silver data and save it to the specified path."""
    logger = get_dagster_logger()

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate dummy data
    data = {
        'id': range(1, 11),
        'name': [f'item_{i}' for i in range(1, 11)],
        'value': np.random.randint(100, 1000, 10),
        'category': np.random.choice(['A', 'B', 'C'], 10),
        'processed_date': pd.date_range(start='2023-01-01', periods=10)
    }

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Generated silver data with {len(df)} rows and saved to {output_path}")

    return df

def generate_gold_data(output_path):
    """Generate dummy gold data and save it to the specified path."""
    logger = get_dagster_logger()

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate dummy data
    data = {
        'id': range(1, 11),
        'name': [f'item_{i}' for i in range(1, 11)],
        'value': np.random.randint(100, 1000, 10),
        'category': np.random.choice(['A', 'B', 'C'], 10),
        'processed_date': pd.date_range(start='2023-01-01', periods=10),
        'aggregated_value': np.random.randint(1000, 5000, 10),
        'status': np.random.choice(['active', 'inactive', 'pending'], 10)
    }

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Generated gold data with {len(df)} rows and saved to {output_path}")

    return df

def generate_all_data(bronze_path, silver_path, gold_path):
    """Generate all dummy data files."""
    logger = get_dagster_logger()
    logger.info("Generating dummy data for all layers...")

    bronze_df = generate_bronze_data(os.path.join(bronze_path, "bronze_data.csv"))
    silver_df = generate_silver_data(os.path.join(silver_path, "silver_data.csv"))
    gold_df = generate_gold_data(os.path.join(gold_path, "gold_data.csv"))

    logger.info("All dummy data generated successfully!")

    return {
        "bronze": bronze_df,
        "silver": silver_df,
        "gold": gold_df
    }