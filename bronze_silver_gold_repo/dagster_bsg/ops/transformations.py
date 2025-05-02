from dagster import op, Output, MetadataValue
import pandas as pd
import numpy as np
from datetime import datetime


@op
def process_customer_data(context, customer_data):
    """
    Process customer data from CSV.

    Args:
        context: Dagster context
        customer_data: DataFrame with customer data

    Returns:
        Processed DataFrame
    """
    return Output(
        customer_data,
        metadata={
            "row_count": len(customer_data),
            "columns": list(customer_data.columns),
            "preview": MetadataValue.md(customer_data.head().to_markdown())
        }
    )

@op
def process_product_data(context, product_data):
    """
    Process product data from CSV.

    Args:
        context: Dagster context
        product_data: DataFrame with product data

    Returns:
        Processed DataFrame
    """
    return Output(
        product_data,
        metadata={
            "row_count": len(product_data),
            "columns": list(product_data.columns),
            "preview": MetadataValue.md(product_data.head().to_markdown())
        }
    )

@op
def enrich_customer_data(context, customer_data):
    """
    Enrich customer data with business logic.

    Args:
        context: Dagster context
        customer_data: DataFrame with customer data

    Returns:
        Enriched DataFrame
    """
    # Create business-ready data
    df = customer_data.copy()

    # Add customer segment based on name length (dummy business logic)
    df['customer_segment'] = df['name'].apply(lambda x: 'Premium' if len(x) > 10 else 'Standard')

    # Add a business-ready timestamp
    df['business_timestamp'] = datetime.now().isoformat()

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@op
def enrich_product_data(context, product_data):
    """
    Enrich product data with business logic.

    Args:
        context: Dagster context
        product_data: DataFrame with product data

    Returns:
        Enriched DataFrame
    """
    # Create business-ready data
    df = product_data.copy()

    # Add price tier based on price (dummy business logic)
    df['price_tier'] = df['price'].apply(lambda x: 'High' if x > 30 else 'Medium' if x > 20 else 'Low')

    # Add a business-ready timestamp
    df['business_timestamp'] = datetime.now().isoformat()

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@op
def create_customer_product_relationship(context, customer_data, product_data):
    """
    Create customer-product relationship data.

    Args:
        context: Dagster context
        customer_data: DataFrame with customer data
        product_data: DataFrame with product data

    Returns:
        Relationship DataFrame
    """
    # Create a relationship between customers and products (dummy data)
    np.random.seed(42)  # For reproducibility

    # Create random relationships
    relationships = []
    for customer_id in customer_data['customer_id']:
        # Each customer has 1-3 random products
        num_products = np.random.randint(1, 4)
        product_ids = np.random.choice(product_data['product_id'], num_products, replace=False)

        for product_id in product_ids:
            relationships.append({
                'customer_id': customer_id,
                'product_id': product_id,
                'relationship_timestamp': datetime.now().isoformat()
            })

    df = pd.DataFrame(relationships)

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@op
def clean_customer_data(context, customer_data):
    """
    Clean and standardize customer data.

    Args:
        context: Dagster context
        customer_data: DataFrame with customer data

    Returns:
        Cleaned DataFrame
    """
    # Clean and standardize the data
    df = customer_data.copy()

    # Standardize phone numbers (remove dashes)
    df['phone'] = df['phone'].str.replace('-', '')

    # Add a standardized timestamp
    df['processed_timestamp'] = datetime.now().isoformat()

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@op
def clean_product_data(context, product_data):
    """
    Clean and standardize product data.

    Args:
        context: Dagster context
        product_data: DataFrame with product data

    Returns:
        Cleaned DataFrame
    """
    # Clean and standardize the data
    df = product_data.copy()

    # Round prices to 2 decimal places
    df['price'] = df['price'].round(2)

    # Add a standardized timestamp
    df['processed_timestamp'] = datetime.now().isoformat()

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )
