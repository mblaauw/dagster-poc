from .transformations import (
    process_customer_data,
    process_product_data,
    enrich_customer_data,
    enrich_product_data,
    create_customer_product_relationship,
    clean_customer_data,
    clean_product_data
)

# Define all ops for the pipeline
bvi_ops = [
    process_customer_data,
    process_product_data,
    enrich_customer_data,
    enrich_product_data,
    create_customer_product_relationship,
    clean_customer_data,
    clean_product_data
]
