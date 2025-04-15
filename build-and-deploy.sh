#!/bin/bash
set -e

# Variables
IMAGE_NAME="dagster-repo:latest"
K8S_NAMESPACE="dagster-poc"  # Change if you're using a different namespace
DAGSTER_DEPLOYMENT_NAME="dagster"
DAGSTER_HELM_RELEASE="dagster"

echo "🚀 Building Docker image..."
docker build -t $IMAGE_NAME .

echo "✅ Docker image built: $IMAGE_NAME"

# Optional: If you're using a local registry, push the image
echo "🚀 Pushing Docker image to local registry..."
docker tag $IMAGE_NAME localhost:5000/$IMAGE_NAME
docker push localhost:5000/$IMAGE_NAME
echo "✅ Docker image pushed to local registry."

echo "🚀 Applying Kubernetes PVCs..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/bronze-pvc.yaml
kubectl apply -f k8s/silver-pvc.yaml
kubectl apply -f k8s/gold-pvc.yaml

echo "✅ PVCs applied."

echo "🚀 Upgrading Dagster Helm release with new image..."
helm upgrade --install $DAGSTER_HELM_RELEASE dagster/dagster \
  --namespace $K8S_NAMESPACE \
  -f k8s/dagster-values.yaml

echo "✅ Dagster Helm release upgraded."

echo "🎉 Build and deploy completed successfully!"
