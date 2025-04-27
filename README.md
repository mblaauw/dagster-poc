# Dagster Project

This project demonstrates a Dagster deployment with a decoupled architecture, separating the infrastructure from the user code in Kubernetes.

## Architecture

The project uses a decoupled architecture where:
- **Infrastructure**: Runs the Dagster webserver, daemon, and PostgreSQL database
- **User Code**: Runs as a separate gRPC server container

This separation allows for:
- Faster iteration on your data pipelines
- Stability of the Dagster infrastructure
- Flexibility to add or swap out multiple user code repositories

## Project Structure

```
.
├── dagster_repo/          # Dagster repository code
│   ├── data_generator.py     # Dummy data generation module
│   ├── bronze_asset.py       # Bronze layer asset
│   ├── silver_asset.py       # Silver layer asset
│   ├── gold_asset.py         # Gold layer asset
│   ├── jobs.py               # Job definitions
│   ├── repository.py         # Repository definition
│   └── resources.py          # Resource definitions
├── k8s/
│   ├── base/                # Base Kubernetes configurations
│   │   ├── namespace.yaml
│   │   ├── pvc.yaml
│   │   └── values.yaml
│   └── infra/               # Infrastructure configuration
│       ├── dagster.yaml     # Dagster configuration
│       ├── workspace.yaml   # Workspace configuration
│       ├── values.yaml      # Helm values for infrastructure
│       └── templates/       # Helm templates
├── scripts/                 # Deployment and utility scripts
│   ├── build-repo.sh        # Build the repository Docker image
│   ├── deploy-dagster.sh    # Deploy Dagster infrastructure
│   ├── deploy-repo.sh       # Deploy the repository
│   ├── remove-dagster.sh    # Remove Dagster infrastructure
│   └── remove-repo.sh       # Remove the repository
├── Dockerfile              # Docker configuration for the repository
└── requirements.txt        # Python dependencies
```

## Features

- **Automatic Data Generation**: The repository includes a data generator module that automatically creates dummy data if it doesn't exist. This eliminates the need for separate data creation steps during deployment.
- **Three-Layer Data Architecture**: Implements a bronze, silver, and gold data architecture with appropriate transformations at each layer.
- **Kubernetes Deployment**: Complete deployment scripts for both infrastructure and user code.
- **Helm Chart**: Custom Helm chart for deploying the Dagster infrastructure.
- **Simplified PVC Management**: PVCs are automatically recreated on each deployment, ensuring a clean state.

## Deployment

### Prerequisites

- Kubernetes cluster
- kubectl configured to access your cluster
- Helm installed
- Docker installed

### Deployment Steps

1. Deploy the Dagster infrastructure:
   ```
   ./scripts/deploy-dagster.sh
   ```

2. Deploy your repository:
   ```
   ./scripts/deploy-repo.sh
   ```

3. Access the Dagster UI at the LoadBalancer IP address.

### Removal

To remove the repository:
```
./scripts/remove-repo.sh
```

To remove the entire Dagster infrastructure:
```
./scripts/remove-dagster.sh
```

## Data Generation

The repository includes an integrated data generator that automatically creates dummy data if it doesn't exist. This happens when:

1. The bronze asset runs and doesn't find the bronze data file
2. The silver asset runs and doesn't find the silver data file
3. The gold asset runs and doesn't find the gold data file

This eliminates the need for separate data creation steps during deployment and ensures that your assets always have data to work with.

## Development

### Building the Repository Image

To build the repository Docker image:
```
./scripts/build-repo.sh
```

### Running Locally

To run the repository locally:
```
dagster dev
```

## Accessing Dagster

Once deployed, the Dagster UI will be available at:
```
http://localhost:30000
```

## Development

### Project Structure

- `dagster_repo/`: Contains the Dagster repository code
  - `bronze_asset.py`: Bronze layer asset definition
  - `silver_asset.py`: Silver layer asset definition
  - `gold_asset.py`: Gold layer asset definition
  - `jobs.py`: Job definitions
  - `repository.py`: Repository configuration

### Adding New Assets

1. Create a new asset file in `dagster_repo/`
2. Define your asset using the Dagster decorators
3. Import and add the asset to the repository in `repository.py`

### Adding New Jobs

1. Define your job in `jobs.py`
2. Add the job to the repository in `repository.py`

### Updating Your Repository

When you make changes to your repository code:

1. Build the updated image:
   ```bash
   ./scripts/build-repo.sh
   ```

2. Deploy the updated repository:
   ```bash
   ./scripts/deploy-repo.sh
   ```

The infrastructure remains running, and your updated pipelines are immediately available.

## Cleanup

To remove the Dagster repository:
```bash
./scripts/remove-repo.sh
```

## Troubleshooting

### Common Issues

1. **Dagster UI not accessible**
   - Check if the Dagster deployment is running:
     ```bash
     kubectl get pods -n dagster-poc
     ```
   - Check the logs:
     ```bash
     kubectl logs -n dagster-poc deployment/dagster-dagster-webserver
     ```

2. **Repository not showing in UI**
   - Check if the repository deployment is running:
     ```bash
     kubectl get pods -n dagster-poc
     ```
   - Check the logs:
     ```bash
     kubectl logs -n dagster-poc deployment/dagster-repo
     ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.