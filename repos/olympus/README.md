# Olympus Data Pipeline

This repository contains a Dagster-based data pipeline implementing a bronze/silver/gold architecture for data processing.

## Architecture Overview

The pipeline follows a three-layer architecture:

1. **Bronze Layer**: Raw data ingestion
   - Ingests data from various sources without transformation
   - Preserves original data format and structure
   - Assets: `bronze_customer_data`, `bronze_product_data`

2. **Silver Layer**: Data cleaning and standardization
   - Applies data quality rules and standardization
   - Handles data type conversions and formatting
   - Assets: `silver_customer_data`, `silver_product_data`

3. **Gold Layer**: Business-ready data
   - Creates business-specific views and aggregations
   - Implements business logic and metrics
   - Assets: `gold_customer_data`, `gold_product_data`, `gold_customer_product_relationship`

## Jobs

The pipeline includes several jobs:

- `bronze_job`: Runs only the bronze layer assets
- `silver_job`: Runs only the silver layer assets
- `gold_job`: Runs only the gold layer assets
- `bvi_job`: Runs the complete pipeline (all layers)

## Running the Pipeline

To run the pipeline:

```bash
dagster dev
```

Then navigate to the Dagster UI at http://localhost:3000 to launch jobs.

## Usage (Local)

```bash
cd repos/olympus
pip install -e .
dagit -w workspace.yaml
```

## Usage (Docker)

```bash
docker build -t olympus .
docker run -p 4000:4000 olympus
```

## Directory structure for multi-repo deployments

Place all project folders inside `/repos/` and use a central `workspace.yaml` to reference each repo if needed.