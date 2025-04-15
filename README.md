# Dagster MVP — Gold/Silver/Bronze Architecture on Kubernetes with PVCs

## 🧠 Objective

Create a **fully local MVP (Minimum Viable Product)** using **Dagster** to demonstrate:
- The **Gold / Silver / Bronze architecture pattern**
- A smooth **developer experience**: from writing assets → dockerizing → deploying to Kubernetes
- Manual **job triggering**, **persistent volume**-based data storage, and **verbose logging**
- Local-only workflow using **VSCode**, **Docker**, **kubectl**, and **Helm** on an M3 MacBook (Orbstack K8s)

---

## 📐 Architecture Overview

| Component               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Developer Environment  | Local laptop with VSCode, Docker, kubectl, Helm installed. No code-server. |
| Kubernetes Cluster     | Local Orbstack K8s cluster. Not included in code but used for deployment.  |
| Dagster                | Deployed via Helm chart. Serves UI, gRPC server, and runs jobs.             |
| Storage                | PVCs simulate object buckets: `bronze`, `silver`, and `gold` layers.        |
| Data Format            | CSV files — simple and readable.                                            |
| Pipeline Triggering    | Fully manual via Dagster UI.                                                |
| CI/CD                  | Manual using a single `build-and-deploy.sh` script.                         |
| Logging                | Enabled and verbose at every pipeline step.                                 |

---

## 🔄 Flow Overview

```plaintext
+------------------+       +----------------+       +---------------+
|  /data/bronze/   |  -->  |  /data/silver/ |  -->  | /data/gold/   |
| bronze_data.csv  |       | transformed    |       | aggregated    |
+------------------+       +----------------+       +---------------+

Developer Flow:
1. Edit Dagster code (VSCode)
2. Run ./build-and-deploy.sh
3. Access Dagster UI
4. Trigger pipeline jobs manually
5. Inspect output files + logs

dagster-poc/
├── Dockerfile
├── build-and-deploy.sh
├── requirements.txt
├── README.md
├── dummy_data/
│   └── bronze_data.csv
├── dagster_project/
│   ├── __init__.py
│   ├── bronze_asset.py
│   ├── silver_asset.py
│   ├── gold_asset.py
│   ├── jobs.py
│   ├── repository.py
│   └── resources.py
└── k8s/
    ├── bronze-pvc.yaml
    ├── silver-pvc.yaml
    ├── gold-pvc.yaml
    └── dagster-values.yaml

# 🧱 Key Components

## 📦 Assets
* **bronze_asset**: Reads `bronze_data.csv` from `/data/bronze/`, logs basic info, returns DataFrame.
* **silver_asset**: Transforms bronze data, adds new column, writes to `/data/silver/silver_data.csv`.
* **gold_asset**: Aggregates silver data, writes to `/data/gold/gold_data.csv`.

## ⚙️ Jobs
* `bronze_to_silver_job`: Runs bronze → silver.
* `silver_to_gold_job`: Runs silver → gold.

## 📦 PVCs
* `bronze-pvc`: Mounted to `/data/bronze/`
* `silver-pvc`: Mounted to `/data/silver/`
* `gold-pvc`: Mounted to `/data/gold/`

Defined as Kubernetes YAML files in `k8s/`.

## 🐳 Docker & Deployment
* **Dockerfile** builds a Dagster gRPC-ready image (`dagster-repo:latest`)
* `build-and-deploy.sh`:
   * Builds image
   * Applies PVCs
   * Installs or upgrades Helm chart for Dagster with mounted volumes

## 🌐 Dagster Helm Configuration
* Uses official Dagster Helm chart: `dagster/dagster`
* Image set to local build
* NodePort enabled on port 30000 (can be changed)
* PVCs mounted to pipeline containers via Helm `values.yaml`

## 🛠️ Developer Experience
1. Work locally in VSCode
2. Modify Python asset or job code
3. Run `./build-and-deploy.sh`
4. Open Dagster UI (`localhost:30000` or port-forward)
5. Trigger jobs manually and inspect logs
6. Check `/data/silver/` and `/data/gold/` directories for output

## 📝 Manual CI/CD Flow
* No automation or GitOps
* One shell script for build & deploy
* Lightweight, fast, and reproducible
* Logs visible both in UI and Kubernetes pod logs

## ✅ Success Criteria
* Developer can fully manage the code → dockerize → deploy → trigger cycle
* Bronze/silver/gold assets are clearly separated
* Output data is correct and stored in mounted PVCs
* Logs clearly reflect each processing stage
* MVP is clean, reproducible, and extensible

## 🔒 Out of Scope
* Authentication / Authorization
* Cloud or external storage
* CI/CD pipelines (only manual)
* Remote code development environments (no code-server)

## 📈 Ready for AI Input
You can now use this markdown file to:
* Scaffold code using AI
* Explain project purpose to team members
* Use it as project documentation for your MVP