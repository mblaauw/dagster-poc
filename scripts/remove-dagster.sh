#!/bin/bash

# Exit on error
set -e

# Variables
K8S_NAMESPACE="dagster-poc"
HELM_RELEASE_NAME="dagster"

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

if ! command_exists helm; then
    echo "Helm is not installed. Please install Helm first."
    exit 1
fi

echo "Removing Dagster repository if it exists..."
"$SCRIPT_DIR/remove-repo.sh"

echo "Uninstalling Dagster Helm release..."
helm uninstall $HELM_RELEASE_NAME -n $K8S_NAMESPACE --ignore-not-found

echo "Removing PVCs..."
kubectl delete pvc bronze-pvc silver-pvc gold-pvc -n $K8S_NAMESPACE --ignore-not-found=true

echo "Removing namespace..."
kubectl delete namespace $K8S_NAMESPACE --ignore-not-found=true

echo "Dagster infrastructure removal completed!"