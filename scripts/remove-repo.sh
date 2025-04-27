#!/bin/bash

# Exit on error
set -e

# Variables
K8S_NAMESPACE="dagster-poc"
HELM_RELEASE_NAME="dagster-repo"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."
if ! command_exists kubectl; then
    echo "kubectl is not installed. Please install kubectl first."
    exit 1
fi

echo "Removing repository deployment..."
if ! kubectl get deployment -n $K8S_NAMESPACE dagster-repo &> /dev/null; then
    echo "Repository deployment not found. Nothing to remove."
    exit 0
fi

# Delete the deployment and service
kubectl delete deployment dagster-repo -n $K8S_NAMESPACE --ignore-not-found
kubectl delete service dagster-repo -n $K8S_NAMESPACE --ignore-not-found

echo "Repository deployment removed successfully!"