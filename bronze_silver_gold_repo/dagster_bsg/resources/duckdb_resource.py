from dagster import resource
import duckdb

@resource
def duckdb_resource():
    conn = duckdb.connect(database=':memory:')
    yield conn
    conn.close()
