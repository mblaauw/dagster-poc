FROM python:3.10-slim

# Install uv (blazing fast package manager)
RUN pip install uv

# Set working directory inside container
WORKDIR /opt/dagster/app

# Copy project files
COPY . .

# Install all dependencies with uv
RUN uv pip install --system --requirement requirements.txt

# Expose the port for Dagster gRPC server
EXPOSE 4000

# Start the Dagster code server (better for hot reload)
CMD ["dagster", "code-server", "start", "--host", "0.0.0.0", "--port", "4000", "--python-file", "repo.py"]
