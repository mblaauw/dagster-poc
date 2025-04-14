from dagster import ConfigurableResource

class DataPaths(ConfigurableResource):
    bronze_path: str = "/data/bronze/"
    silver_path: str = "/data/silver/"
    gold_path: str = "/data/gold/"
