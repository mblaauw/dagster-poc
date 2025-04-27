from dagster import asset, AssetIn
from ..ops.transformations import clean_customer_data, clean_product_data

@asset(
    group_name="silver",
    description="Cleaned and standardized customer data",
    ins={
        "bronze_customer_data": AssetIn(key="bronze_customer_data")
    }
)
def silver_customer_data(bronze_customer_data):
    """
    Asset for silver customer data.
    """
    return clean_customer_data(bronze_customer_data)

@asset(
    group_name="silver",
    description="Cleaned and standardized product data",
    ins={
        "bronze_product_data": AssetIn(key="bronze_product_data")
    }
)
def silver_product_data(bronze_product_data):
    """
    Asset for silver product data.
    """
    return clean_product_data(bronze_product_data)