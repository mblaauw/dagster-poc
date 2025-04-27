from dagster import resource

@resource
def db_connection():
    return "dummy_connection"