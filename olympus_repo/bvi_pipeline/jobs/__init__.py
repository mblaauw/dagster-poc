from .bronze import bronze_job
from .silver import silver_job
from .gold import gold_job
from .complete import bvi_job

# Define all jobs for the pipeline
bvi_jobs = [
    bronze_job,
    silver_job,
    gold_job,
    bvi_job
]
