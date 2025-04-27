#!/bin/bash

# Exit on error
set -e

# Variables
IMAGE_NAME="dagster-repo:latest"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

echo "Building Docker image..."
docker build -t $IMAGE_NAME "$PROJECT_ROOT"

echo "Docker image built: $IMAGE_NAME"