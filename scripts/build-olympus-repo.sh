#!/bin/bash

set -euo pipefail

# Settings
IMAGE_NAME="olympus-repo:latest"

# DEPLOYMENT_NAME="olympus-repo"
# DEPLOYMENT_FILE="../infra/olympus-repo-deployment.yaml"

DOCKERFILE_PATH="../repos/olympus/Dockerfile"
CONTEXT_PATH="../repos/olympus/"

NAMESPACE="dagster-poc"

echo "🔨 Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" "$CONTEXT_PATH"
echo "✅ Successfully built $IMAGE_NAME"

# echo "🚀 Applying Kubernetes deployment"
# kubectl apply -f "$DEPLOYMENT_FILE" -n "$NAMESPACE"

# echo "♻️  Restarting deployment to pick up latest image"
# kubectl rollout restart deployment/"$DEPLOYMENT_NAME" -n "$NAMESPACE"

# echo "⏳ Waiting for rollout to finish..."
# kubectl rollout status deployment/"$DEPLOYMENT_NAME" -n "$NAMESPACE"

echo "✅ Olympus deployed and running"