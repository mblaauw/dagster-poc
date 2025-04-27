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

if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Dagster is running
if ! kubectl get deployment -n $K8S_NAMESPACE dagster-dagster-webserver &> /dev/null; then
    echo "Dagster infrastructure is not running. Please run ./scripts/deploy-dagster.sh first."
    exit 1
fi

echo "Building repository image..."
"$SCRIPT_DIR/build-repo.sh"

echo "Creating repository deployment..."
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dagster-repo
  namespace: $K8S_NAMESPACE
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dagster-repo
  template:
    metadata:
      labels:
        app: dagster-repo
    spec:
      containers:
      - name: dagster-repo
        image: dagster-repo:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 3030
        env:
        - name: DAGSTER_HOME
          value: /opt/dagster/dagster_home
        - name: DAGSTER_POSTGRES_USER
          value: dagster
        - name: DAGSTER_POSTGRES_PASSWORD
          value: dagster
        - name: DAGSTER_POSTGRES_DB
          value: dagster
        - name: DAGSTER_POSTGRES_HOST
          value: dagster-postgresql
        volumeMounts:
        - name: bronze-volume
          mountPath: /data/bronze
        - name: silver-volume
          mountPath: /data/silver
        - name: gold-volume
          mountPath: /data/gold
      volumes:
      - name: bronze-volume
        persistentVolumeClaim:
          claimName: bronze-pvc
      - name: silver-volume
        persistentVolumeClaim:
          claimName: silver-pvc
      - name: gold-volume
        persistentVolumeClaim:
          claimName: gold-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: dagster-repo
  namespace: $K8S_NAMESPACE
spec:
  selector:
    app: dagster-repo
  ports:
  - port: 3030
    targetPort: 3030
EOF

echo "Waiting for repository deployment to be ready..."
kubectl wait --for=condition=available deployment/dagster-repo -n $K8S_NAMESPACE --timeout=300s

echo "Repository deployment completed!"
echo "Your repository is now available in the Dagster UI."
echo "The dummy data will be automatically generated when you run your assets."