from .bronze import bronze_customer_data, bronze_product_data
from .silver import silver_customer_data, silver_product_data
from .gold import gold_customer_data, gold_product_data, gold_customer_product_relationship

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
