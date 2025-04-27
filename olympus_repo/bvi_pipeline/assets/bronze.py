from dagster import asset
from ..ops.transformations import process_customer_data, process_product_data
import os
import pandas as pd


def read_csv_file(context, file_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    full_path = os.path.join(data_dir, file_path)
    df = pd.read_csv(full_path)
    return df


@asset(
    group_name="bronze",
    description="Raw data ingestion from source systems"
)
def bronze_customer_data():
    """
    Asset for bronze customer data.
    """
    df = read_csv_file("customer_data.csv")
    return process_customer_data(df)

@asset(
    group_name="bronze",
    description="Raw product data ingestion"
)
def bronze_product_data():
    """
    Asset for bronze product data.
    """
    df = read_csv_file("product_data.csv")
    return process_product_data(df)