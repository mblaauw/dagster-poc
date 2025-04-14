# Use official Python 3.10 slim base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DAGSTER_HOME=/opt/dagster/dagster_home

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Create Dagster home directory
RUN mkdir -p $DAGSTER_HOME

# Expose port (not strictly necessary for gRPC)
EXPOSE 4000

# Set entrypoint to Dagster gRPC server
ENTRYPOINT ["dagster", "api", "grpc", "-m", "dagster_project"]
