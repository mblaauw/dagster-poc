#!/bin/bash
set -e

echo "Creating dagster-poc namespace..."
kubectl create namespace dagster-poc --dry-run=client -o yaml | kubectl apply -f -

echo "Installing Dagster using Helm..."
helm upgrade --install dagster dagster/dagster \
  --namespace dagster-poc \
  --create-namespace \
  --values ../infra/values.yaml \
  --atomic \
  --timeout 2m

echo "Waiting for all pods to be ready..."
kubectl wait --for=condition=ready pod --all -n dagster-poc --timeout=30s

echo "Dagster has been installed successfully!"
echo "To access the Dagster UI, run:"
echo "kubectl port-forward svc/dagster-dagster-webserver 8080:80 -n dagster-poc"
echo "Then visit http://localhost:8080 in your browser"