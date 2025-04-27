# Dagster POC

A proof of concept for Dagster deployment using Helm.

## Project Structure

```
.
├── helm/           # Helm chart files
├── repos/          # Dagster repositories
│   └── olympus/    # Olympus repository
│       └── bvi-pipeline/  # BVI Pipeline subproject
└── script/         # Installation scripts
```

## Installation

To install Dagster:

```bash
./script/install-dagster.sh
```

To uninstall Dagster:

```bash
./script/uninstall-dagster.sh
```