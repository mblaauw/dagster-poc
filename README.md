# Dagster PoC — Bronze / Silver / Gold Architecture

## 🎯 Objective

This is a Proof of Concept (PoC) for demonstrating data pipeline development with Dagster, following the Bronze / Silver / Gold architecture pattern.

The goal is to showcase:
- Developer experience: from writing code → dockerize → deploy → run manually
- Manual CI/CD flow using a simple shell script
- Clear separation of assets per layer (bronze, silver, gold)
- PVC-backed storage instead of object storage
- Manual triggering of pipelines via Dagster UI
- Detailed logging for visibility
- Local Kubernetes cluster (Orbstack)

---

## 🗂️ Project Structure

dagster-poc/ ├── Dockerfile ├── build-and-deploy.sh ├── requirements.txt ├── dummy_data/ │ └── bronze_data.csv ├── dagster_project/ │ ├── init.py │ ├── repository.py │ ├── jobs.py │ ├── bronze_asset.py │ ├── silver_asset.py │ ├── gold_asset.py │ └── resources.py └── k8s/ ├── bronze-pvc.yaml ├── silver-pvc.yaml ├── gold-pvc.yaml └── dagster-values.yaml


## 🚀 Developer Workflow

1. **Edit Code Locally**
   - Open the project in VSCode.
   - Modify or add Dagster assets, jobs, or resources.

2. **Build and Deploy**
   - Run:
     ```bash
     ./build-and-deploy.sh
     ```

3. **Access Dagster UI**
   - Open the Dagster UI in your browser.
   - URL will depend on your Kubernetes setup (NodePort / Ingress).

4. **Run Pipelines Manually**
   - Materialize `bronze_to_silver_job`.
   - Materialize `silver_to_gold_job`.

5. **Check Output**
   - Inspect data files in your PVC-mounted directories:
     - `/data/bronze/`
     - `/data/silver/`
     - `/data/gold/`

6. **Observe Logs**
   - Logs are visible in the Dagster UI and Kubernetes pod logs.

---

## 🧩 Notes

- Data format: CSV
- PVCs are used for shared storage, not MinIO or cloud buckets.
- Pipelines are manually triggered — no sensors or schedules.
- CI/CD is manual via the shell script.
- Logging is enabled for maximum observability.

---

## 📦 Dependencies

See `requirements.txt` for Python dependencies.

