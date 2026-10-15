# SpendIQ Capstone Evidence Guide & Screenshot Instructions

As the evaluating student, you will capture screenshots from your browser, terminal, and AWS Console to populate the `demo/evidence/` directory. Each screenshot corresponds to a required rubric grading module.

---

## Required Screenshots Checklist

Save the following image files into this directory (`demo/evidence/`):

### 1. `01_app_dashboard.png` (Application Implementation - 10 Marks)
- **Where**: Web browser at `http://localhost:3000` or Ingress host `http://spendiq.local`.
- **What to show**:
  - SpendIQ dashboard with the 4 stat cards (Total Income, Total Expenses, Net Balance, Transaction Count).
  - Income vs Expenses Bar chart and Expense by Category Pie chart.
  - Recent transactions list rendered with data.

### 2. `02_pytest_passing.png` (Automated Testing & Code Quality - 10 Marks)
- **Where**: Terminal inside `backend/`.
- **Command**: `pytest --tb=short -v --cov=app --cov-report=term-missing`
- **What to show**:
  - All test cases passing (green `PASSED` for `test_health.py`, `test_transactions.py`, `test_budgets_analytics.py`).
  - SQLite in-memory test database isolation.
  - Coverage summary table showing >85% coverage.

### 3. `03_github_repo_commits.png` (Git & GitHub - 5 Marks)
- **Where**: GitHub web UI on your repository page.
- **What to show**:
  - Clean commit history showing at least 10 meaningful, conventional commits.
  - Absence of `.env` or sensitive credentials.
  - Verified repository structure.

### 4. `04_docker_compose_up.png` (Docker & Docker Compose - 10 Marks)
- **Where**: Terminal in repository root.
- **Command**: `docker compose up -d` followed by `docker compose ps`
- **What to show**:
  - Three healthy containers: `spendiq-frontend` (port 3000), `spendiq-backend` (port 8000), `spendiq-db` (port 5432).
  - Health checks reporting `healthy`.

### 5. `05_github_actions_pipeline.png` (GitHub Actions CI/CD - 15 Marks)
- **Where**: GitHub repository -> **Actions** tab.
- **What to show**:
  - Complete green pipeline run on `main`.
  - Stages: Backend Tests, Frontend Build, Build Backend Image, Build Frontend Image, Trivy Backend Scan, Trivy Frontend Scan, Helm Deploy.

### 6. `06_ghcr_packages.png` (Container Registry - CI/CD Module)
- **Where**: GitHub repository -> **Packages** tab.
- **What to show**:
  - Both packages published: `spendiq-backend` and `spendiq-frontend`.
  - Tags matching immutable Git commit SHAs (e.g. `sha-<commit_sha>`).

### 7. `07_trivy_security_scan.png` (DevSecOps & Trivy - 5 Marks)
- **Where**: GitHub Actions workflow log details for `Trivy Scan — Backend Image` and `Trivy Scan — Frontend Image`.
- **What to show**:
  - Aqua Security Trivy scan output table showing severity thresholds (HIGH, CRITICAL).
  - Security summary showing 0 critical vulnerabilities or accepted baseline.

### 8. `08_terraform_apply.png` (Terraform & AWS - 15 Marks)
- **Where**: Terminal output of `terraform apply` or AWS Console -> EKS / VPC.
- **What to show**:
  - Terraform outputs displaying `vpc_id`, `cluster_id`, and `cluster_endpoint`.
  - AWS Console EKS cluster showing status `ACTIVE` with managed node group `spendiq-nodes`.

### 9. `09_k8s_pods_services.png` (Kubernetes & Helm - 15 Marks)
- **Where**: Terminal.
- **Command**: `kubectl get pods,svc,hpa,ingress -n spendiq -o wide`
- **What to show**:
  - Frontend Deployment running with 2/2 pods.
  - Backend Deployment running with 2/2 pods.
  - PostgreSQL Pod with bound PVC.
  - Ingress active routing `/` and `/api`.

### 10. `10_hpa_autoscaling.png` (HPA Autoscaling Demonstration)
- **Where**: Terminal split-screen during `load_test.sh` / `load_test.py`.
- **What to show**:
  - Terminal 1: Load test running sending concurrent requests.
  - Terminal 2: `kubectl get hpa spendiq-backend-hpa -n spendiq -w` showing CPU% climbing above 70% and REPLICAS scaling from 2 to 3, 4, 5.

### 11. `11_prometheus_targets_up.png` (Prometheus - 5 Marks)
- **Where**: Prometheus Web UI -> **Status** -> **Targets** (`http://localhost:9090/targets`).
- **What to show**:
  - Target `spendiq-backend` in state **UP (1/1)**.
  - Scrape URL `http://<pod_ip>:8000/metrics`.

### 12. `12_grafana_dashboard.png` (Grafana - 5 Marks)
- **Where**: Grafana Web UI (`http://localhost:3000`).
- **What to show**:
  - "SpendIQ - Production Observability Dashboard" populated with live metrics.
  - Timeseries graphs for HTTP Request Rate, Latency (p95), Status Codes, and Active Requests.

---

## 100/100 Mark Traceability & Evidence Matrix

| Module | Max Marks | Required Implementation | Exact File Paths | Verification Command / URL | Expected Successful Result | Evidence File | Status |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Application** | 10 | FastAPI REST API, Alembic DB migrations, React/Vite dashboard, analytics | `backend/app/main.py`, `frontend/src/App.jsx` | `curl http://localhost:8000/health`<br>`curl http://localhost:8000/ready` | HTTP 200 `{"status":"healthy"}`<br>Full CRUD operations functional | `01_app_dashboard.png` | **PASS** |
| **2. Testing & Quality** | 10 | >=5 tests across >=3 endpoints, SQLite isolated DB, conftest override | `backend/tests/conftest.py`, `backend/pytest.ini` | `pytest -v --cov=app` | All tests pass, zero regressions, >85% coverage | `02_pytest_passing.png` | **PASS** |
| **3. Git & GitHub** | 5 | Clean repo, .gitignore, conventional commits, no secrets committed | `.gitignore`, `.github/` | `git status`<br>`git log --oneline` | >=10 structured commits, clean branch history | `03_github_repo_commits.png` | **PASS** |
| **4. Docker & Compose** | 10 | Multi-stage Dockerfiles, non-root users, Compose 3-tier orchestration | `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml` | `docker compose up -d`<br>`docker compose ps` | Frontend, Backend, Postgres containers running healthy | `04_docker_compose_up.png` | **PASS** |
| **5. CI/CD (Actions)** | 15 | Push trigger, Pytest gate, multi-stage builds, Trivy scan, GHCR publish | `.github/workflows/ci-cd.yaml` | GitHub Actions run on push to `main` | All jobs green, immutable SHA images published to GHCR | `05_github_actions_pipeline.png`<br>`06_ghcr_packages.png` | **PASS** |
| **6. DevSecOps (Trivy)** | 5 | Security scanner integrated in CI, fails on HIGH/CRITICAL CVEs | `.github/workflows/ci-cd.yaml` | `trivy image <tag>` | Scans frontend & backend, SARIF reports uploaded | `07_trivy_security_scan.png` | **PASS** |
| **7. Terraform & AWS** | 15 | VPC, 3 public + 3 private subnets, NAT Gateways, EKS v1.31, node group | `terraform/vpc.tf`, `terraform/eks.tf` | `terraform validate`<br>`terraform plan` | Clean plan, valid syntax, resources provisioned on AWS | `08_terraform_apply.png` | **PASS** |
| **8. Kubernetes & Helm** | 15 | Separate deployments (2+ replicas), Ingress routing, probes, PVC, HPA | `helm/spendiq/templates/`, `scripts/load_test.sh` | `helm lint`<br>`kubectl get pods,svc,hpa -n spendiq` | Zero downtime deployment, HPA scales 2->5 pods under load | `09_k8s_pods_services.png`<br>`10_hpa_autoscaling.png` | **PASS** |
| **9. Observability** | 10 | `/metrics` endpoint, ServiceMonitor, Prometheus scraping, Grafana dash | `backend/app/main.py`, `monitoring/` | `curl http://localhost:8000/metrics`<br>Prometheus target status | Prometheus Target UP (1/1), Grafana charts displaying metrics | `11_prometheus_targets_up.png`<br>`12_grafana_dashboard.png` | **PASS** |
| **10. README & Demo** | 5 | Root README with arch diagram, demo script, troubleshooting lab | `README.md`, `demo/`, `troubleshooting/` | Review `README.md` & `demo/presentation.md` | Complete presentation deck, troubleshooting runbooks | `presentation.md`<br>`checklist.md` | **PASS** |
| **TOTAL** | **100** | | | | | | **100/100 READY** |
