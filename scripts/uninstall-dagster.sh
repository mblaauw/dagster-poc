#!/bin/bash
set -e

echo "Uninstalling Dagster..."
helm uninstall dagster --namespace dagster-poc

echo "Waiting for pods to terminate..."
kubectl wait --for=delete pod --all -n dagster-poc --timeout=300s || true

echo "Do you want to delete the dagster-poc namespace? (y/N)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    echo "Deleting namespace..."
    kubectl delete namespace dagster-poc
    echo "Namespace deleted."
else
    echo "Namespace 'dagster-poc' has been preserved."
fi

echo "Dagster has been uninstalled successfully!"