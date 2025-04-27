from ..ops.transformations import enrich_customer_data, enrich_product_data, create_customer_product_relationship
from dagster import asset, AssetIn

@asset(
    group_name="gold",
    description="Business-ready customer data with enriched information",
    ins={
        "silver_customer_data": AssetIn(key="silver_customer_data")
    }
)
def gold_customer_data(silver_customer_data):
    """
    Asset for gold customer data.
    """
    return enrich_customer_data(silver_customer_data)

@asset(
    group_name="gold",
    description="Business-ready product data with enriched information",
    ins={
        "silver_product_data": AssetIn(key="silver_product_data")
    }
)
def gold_product_data(silver_product_data):
    """
    Asset for gold product data.
    """
    return enrich_product_data(silver_product_data)

@asset(
    group_name="gold",
    description="Business-ready customer-product relationship data",
    ins={
        "gold_customer_data": AssetIn(key="gold_customer_data"),
        "gold_product_data": AssetIn(key="gold_product_data")
    }
)
def gold_customer_product_relationship(gold_customer_data, gold_product_data):
    """
    Asset for gold customer-product relationship data.
    """
    return create_customer_product_relationship(gold_customer_data, gold_product_data)