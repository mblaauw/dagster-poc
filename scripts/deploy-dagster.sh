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

# Add Dagster Helm repository if not already added
if ! helm repo list | grep -q "^dagster"; then
    echo "Adding Dagster Helm repository..."
    helm repo add dagster https://dagster.github.io/helm
    helm repo update
fi

echo "Creating namespace if it doesn't exist..."
kubectl create namespace $K8S_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "Removing existing PVCs if they exist..."
kubectl delete pvc bronze-pvc silver-pvc gold-pvc -n $K8S_NAMESPACE --ignore-not-found=true

echo "Creating new PVCs..."
kubectl apply -f "$PROJECT_ROOT/k8s/base/pvc.yaml" -n $K8S_NAMESPACE

echo "Waiting for PVCs to be created..."
kubectl wait --for=condition=Bound pvc/bronze-pvc pvc/silver-pvc pvc/gold-pvc -n $K8S_NAMESPACE --timeout=300s

echo "Installing/upgrading Dagster infrastructure..."
helm upgrade --install $HELM_RELEASE_NAME dagster/dagster \
  --namespace $K8S_NAMESPACE \
  -f "$PROJECT_ROOT/k8s/infra/values.yaml" \
  --wait

echo "Dagster infrastructure deployment completed!"
echo "To deploy your repository, run: ./scripts/deploy-repo.sh"