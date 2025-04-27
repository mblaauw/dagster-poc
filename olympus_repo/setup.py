from setuptools import setup, find_packages

setup(
    name="olympus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "pandas",
        "requests",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
            "dagster-dbt",
            "dagster-postgres",
            "dagster-snowflake",
            "dagster-aws",
        ],
    },
)