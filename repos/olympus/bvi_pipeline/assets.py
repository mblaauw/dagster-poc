from dagster import asset, AssetIn, Output, MetadataValue
import pandas as pd
import numpy as np
from datetime import datetime

# Bronze layer - Raw data ingestion
@asset(
    group_name="bronze",
    description="Raw data ingestion from source systems"
)
def bronze_customer_data():
    # Dummy data for demonstration
    data = {
        'customer_id': [1, 2, 3, 4, 5],
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Davis'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com', 'charlie@example.com'],
        'phone': ['123-456-7890', '234-567-8901', '345-678-9012', '456-789-0123', '567-890-1234'],
        'raw_timestamp': [datetime.now().isoformat() for _ in range(5)]
    }
    df = pd.DataFrame(data)

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@asset(
    group_name="bronze",
    description="Raw product data ingestion"
)
def bronze_product_data():
    # Dummy data for demonstration
    data = {
        'product_id': [101, 102, 103, 104, 105],
        'name': ['Widget A', 'Widget B', 'Widget C', 'Widget D', 'Widget E'],
        'price': [10.99, 20.99, 30.99, 40.99, 50.99],
        'category': ['Electronics', 'Electronics', 'Home', 'Home', 'Office'],
        'raw_timestamp': [datetime.now().isoformat() for _ in range(5)]
    }
    df = pd.DataFrame(data)

    return Output(
        df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

# Silver layer - Cleaned and standardized data
@asset(
    group_name="silver",
    description="Cleaned and standardized customer data",
    ins={
        "bronze_customer_data": AssetIn(key="bronze_customer_data")
    }
)
def silver_customer_data(bronze_customer_data):
    # Clean and standardize the data
    df = bronze_customer_data.copy()

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

@asset(
    group_name="silver",
    description="Cleaned and standardized product data",
    ins={
        "bronze_product_data": AssetIn(key="bronze_product_data")
    }
)
def silver_product_data(bronze_product_data):
    # Clean and standardize the data
    df = bronze_product_data.copy()

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

# Gold layer - Business-ready data
@asset(
    group_name="gold",
    description="Business-ready customer data with enriched information",
    ins={
        "silver_customer_data": AssetIn(key="silver_customer_data")
    }
)
def gold_customer_data(silver_customer_data):
    # Create business-ready data
    df = silver_customer_data.copy()

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

@asset(
    group_name="gold",
    description="Business-ready product data with enriched information",
    ins={
        "silver_product_data": AssetIn(key="silver_product_data")
    }
)
def gold_product_data(silver_product_data):
    # Create business-ready data
    df = silver_product_data.copy()

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

@asset(
    group_name="gold",
    description="Business-ready customer-product relationship data",
    ins={
        "gold_customer_data": AssetIn(key="gold_customer_data"),
        "gold_product_data": AssetIn(key="gold_product_data")
    }
)
def gold_customer_product_relationship(gold_customer_data, gold_product_data):
    # Create a relationship between customers and products (dummy data)
    np.random.seed(42)  # For reproducibility

    # Create random relationships
    relationships = []
    for customer_id in gold_customer_data['customer_id']:
        # Each customer has 1-3 random products
        num_products = np.random.randint(1, 4)
        product_ids = np.random.choice(gold_product_data['product_id'], num_products, replace=False)

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

# Define all assets for the pipeline


bvi_assets = [
    bronze_customer_data,
    bronze_product_data,
    silver_customer_data,
    silver_product_data,
    gold_customer_data,
    gold_product_data,
    gold_customer_product_relationship
]
