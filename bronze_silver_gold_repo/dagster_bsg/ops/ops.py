from dagster import op, In, Out
from deltalake import DeltaTable, write_deltalake
import polars as pl
import duckdb


@op(out=Out())
def write_sample_data_to_delta():
    df = pl.DataFrame({
        "id": [1, 2, 3],
        "value": ["a", "b", "c"]
    })
    path = "s3://my-delta-bucket/sample_table"
    write_deltalake(path, df.to_arrow(), mode="overwrite")
    return path

@op(ins={"table_path": In()}, out=Out())
def read_from_delta(table_path: str):
    dt = DeltaTable(table_path)
    df = pl.from_arrow(dt.to_pyarrow_table())
    print(df)

@op
def optimize_table():
    dt = DeltaTable("s3://bucket/path")
    dt.vacuum(retention_hours=1)  # Cleans old files
    # No built-in compaction yet; you'd rewrite using DuckDB

@op
def write_raw_delta():
    df = pl.DataFrame({"region": ["EU", "US", "EU"], "sales": [100, 200, 150]})
    write_deltalake("s3://my-bucket/bronze/sales", df, mode="overwrite")
    return "s3://my-bucket/bronze/sales"

@op
def process_with_duckdb(path: str):
    con = duckdb.connect()
    # DuckDB reads Delta via Parquet
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(f"""
        CREATE VIEW sales AS SELECT * FROM parquet_scan('{path}/*.parquet')
    """)
    result = con.execute("""
        SELECT region, SUM(sales) as total_sales
        FROM sales
        GROUP BY region
    """).fetchdf()
    return result