# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
RUN poetry install --no-root

# Expose Dagster webserver port
EXPOSE 3000

# Command to run Dagster webserver and daemon
CMD ["dagster", "dev"]
