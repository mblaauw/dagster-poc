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
# echo "🚀 Pushing Docker image to local registry..."
# docker tag $IMAGE_NAME localhost:5000/$IMAGE_NAME
# docker push localhost:5000/$IMAGE_NAME
# echo "✅ Docker image pushed to local registry."

echo "🚀 Applying Kubernetes PVCs..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/bronze-pvc.yaml
kubectl apply -f k8s/silver-pvc.yaml
kubectl apply -f k8s/gold-pvc.yaml

echo "✅ PVCs applied."

# Create a temporary directory to copy the dummy data
echo "🚀 Initializing dummy data..."
TEMP_DIR=$(mktemp -d)
cp dummy_data/bronze_data.csv $TEMP_DIR/

# Create a simple pod to copy data to PVC
cat << EOF > $TEMP_DIR/copy-data-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: init-bronze-data
  namespace: $K8S_NAMESPACE
spec:
  template:
    spec:
      containers:
      - name: init-data
        image: busybox
        command: ["/bin/sh", "-c", "mkdir -p /data/bronze && cp /tmp/bronze_data.csv /data/bronze/"]
        volumeMounts:
        - name: bronze-volume
          mountPath: /data/bronze
        - name: data-volume
          mountPath: /tmp
      restartPolicy: Never
      volumes:
      - name: bronze-volume
        persistentVolumeClaim:
          claimName: bronze-pvc
      - name: data-volume
        configMap:
          name: bronze-data-configmap
  backoffLimit: 2
EOF

# Create configmap with the data
kubectl -n $K8S_NAMESPACE create configmap bronze-data-configmap --from-file=$TEMP_DIR/bronze_data.csv

# Apply the job
kubectl apply -f $TEMP_DIR/copy-data-job.yaml

# Wait for the job to complete
echo "⏳ Waiting for data initialization to complete..."
kubectl -n $K8S_NAMESPACE wait --for=condition=complete job/init-bronze-data --timeout=60s
echo "✅ Data initialization completed."

# Cleanup temporary files
rm -rf $TEMP_DIR

echo "🚀 Upgrading Dagster Helm release with new image..."
helm upgrade --install $DAGSTER_HELM_RELEASE dagster/dagster \
  --namespace $K8S_NAMESPACE \
  -f k8s/dagster-values.yaml

echo "✅ Dagster Helm release upgraded."

echo "🎉 Build and deploy completed successfully!"