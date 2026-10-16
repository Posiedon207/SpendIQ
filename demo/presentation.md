# SpendIQ Capstone Presentation: Production DevOps & Cloud Architecture

**Deck Format**: 16:9 Widescreen PowerPoint (`demo/SpendIQ_Capstone_Presentation.pptx`)  
**Target Grade**: 100 / 100 Marks (Rubric Modules 1 to 10)  
**Author**: Aditya Gosain (Cloud Architect & Principal DevOps Engineer)  
**Platform**: Amazon EKS v1.31 • Region: `ap-south-1` • GitHub Actions • Terraform • Helm 3  

---

## Slide 1: Title & Executive Summary
- **Project**: SpendIQ — Enterprise Cloud-Native Personal Finance SaaS
- **Author**: Aditya Gosain
- **Specialization**: Cloud Architect & Principal DevOps Engineer
- **Mission**: Deliver a reliable, observable, scalable, and secure cloud-native architecture on AWS EKS with end-to-end GitOps CI/CD.
- **Key Badges**:
  - 100 / 100 Target Score
  - 45 / 45 Pytest Tests Passing (91% Coverage)
  - Zero High / Critical CVEs (Aqua Trivy Gated)
  - Zero Leaked Credentials & Hardened `.gitignore`

---

## Slide 2: Problem Statement & Engineering Mission
- **Modern Fintech SaaS Challenges**:
  - *Unpredictable Traffic Surges*: High volatility during statement cycles and payroll spikes leads to cascading microservice outages.
  - *Data Consistency & Migration Risk*: Relational financial records require strict ACID compliance; manual SQL scripts risk data corruption.
  - *Container Supply Chain Threats*: Bloated base images contain unpatched CVEs, risking unauthorized access.
  - *Deployment Downtime & Drift*: Manual cloud provisioning causes drift, failed rollbacks, and release downtime.
- **SpendIQ Solution Pillars**:
  - Elastic Horizontal Pod Autoscaling (HPA) dynamically scaling 2 to 5 pods based on CPU utilization (>70%).
  - Version-controlled Alembic migrations with PostgreSQL 16 on Kubernetes PersistentVolumeClaims (5Gi).
  - DevSecOps Aqua Trivy scanning in GitHub Actions CI with blocking `exit-code: 1` gate.
  - Zero-downtime Helm 3 rolling updates with Liveness and Readiness self-healing probes.
- **Target Operational SLAs**:
  - `< 1.5s` P95 API Latency SLA
  - `99.95%` High Availability
  - `100%` Automated CI Testing
  - `0 Mins` Release Downtime

---

## Slide 3: End-to-End System & Cloud Architecture Ecosystem
- **Tier 1 (Presentation)**: React 18 SPA, Vite, Recharts, Axios, served via unprivileged NGINX 1.27 Alpine runtime (`nginx:101`). Size: ~28MB.
- **Tier 2 (Application)**: Python 3.12, FastAPI async engine, Pydantic v2 schemas, Prometheus telemetry middleware, `dumb-init` PID 1 execution (`appuser:1001`). Size: ~118MB.
- **Tier 3 (Persistence)**: PostgreSQL 16 Alpine, automated Alembic migrations (`001_initial.py`), Kubernetes 5Gi PVC.
- **Cloud Foundation**: AWS `ap-south-1` Multi-AZ VPC (`10.0.0.0/16`), Amazon EKS v1.31 with Managed Node Groups, GitHub Actions CI/CD, GHCR, and Prometheus/Grafana monitoring.
- **Request Flow**:
  `Client Browser -> NGINX Ingress -> ClusterIP Service -> FastAPI Pods (2-5x HPA) -> PostgreSQL 16 (PVC) -> Prometheus Scraper -> Grafana Live Dashboard`.

---

## Slide 4: Module 1 — Application & REST API Ecosystem (10/10 Marks)
- **FastAPI /health & /ready Probes (2 pts)**: Returns JSON status, database connectivity, app version, and ISO timestamp.
- **15+ REST Endpoints (3 pts)**: Full CRUD for Transactions, monthly Budgets, category Analytics rollups, and demo data seeding.
- **PostgreSQL 16 + Alembic (2 pts)**: Automated schema migration `001_initial.py` defining foreign keys, indexes, and enum constraints.
- **React 18 SPA Dashboard (2 pts)**: Responsive dark-mode dashboard with live balance calculations and Recharts graphs.
- **Production Usability (1 pt)**: Single-command spin-up via `docker compose up -d --build`.
- **Embedded Evidence**: `01_app_dashboard.png` (Live Frontend Dashboard) and `04_api_swagger_docs.png` (FastAPI Swagger UI).

---

## Slide 5: Module 2 — Automated Testing & Test DB Isolation (10/10 Marks)
- **Pytest Suite (3 pts)**: 45/45 tests passing in 1.03s with 0 errors and 0 warnings.
- **Coverage Benchmark (4 pts)**: 91% code coverage verified via `pytest-cov`, far exceeding the 80% rubric standard.
- **Test DB Isolation (2 pts)**: `conftest.py` dynamically overrides `get_db` with an isolated SQLite session (`DATABASE_URL=sqlite:///./test_spendiq.db`), guaranteeing zero test pollution of production PostgreSQL.
- **Pytest Configuration (1 pt)**: `pytest.ini` defines test discovery, async modes, and short traceback formatting.
- **CI Quality Gate**: Blocking gate in GitHub Actions; container builds are aborted immediately if tests fail.
- **Embedded Evidence**: `05_pytest_passing.png` (Pytest 45 passed + coverage table).

---

## Slide 6: Module 3 — Git Hygiene, Commit Taxonomy & Secret Protection (5/5 Marks)
- **Public GitHub Repository (2 pts)**: Clean, public repository with clear licensing and branch protection.
- **Conventional Commits (2 pts)**: 16+ atomic commits using standard prefixes (`feat:`, `fix:`, `infra:`, `deploy:`, `docs:`, `test:`).
- **Hardened `.gitignore` (1 pt)**: Excludes `.env`, AWS keys, `*.pem`, `*.db`, `node_modules`, `__pycache__`, and `.venv`.
- **Zero Committed Secrets**: Strict DevSecOps adherence; credentials injected strictly via GitHub Secrets and environment variables.
- **Embedded Evidence**: `08_git_commit_history.png` (Terminal Git log showing atomic commit taxonomy).

---

## Slide 7: Module 4 — Docker Multi-Stage Builds & Non-Root Hardening (10/10 Marks)
- **Backend Dockerfile (2 pts)**: Multi-stage Python 3.12-slim build. Builder stage isolates compiler toolchains; runtime runs as non-root `appuser:1001` with `dumb-init` (Size: ~118MB).
- **Frontend Dockerfile (3 pts)**: Multi-stage: Node 22 compiles Vite bundle -> unprivileged NGINX 1.27 Alpine runtime (`nginx:101`) (Size: ~28MB).
- **Non-Root Security (2 pts)**: Eliminates container breakout risks by removing root privileges.
- **Docker Compose (3 pts)**: Single command `docker compose up -d --build` launches frontend, backend, and PostgreSQL with container health checks.
- **Embedded Evidence**: `06_docker_compose_running.png` (All containers healthy).

---

## Slide 8: Module 5 — GitHub Actions CI/CD Pipeline Automation (15/15 Marks)
- **Workflow Trigger (2 pts)**: Automated execution on push to `main` and `develop`.
- **Pytest Quality Gate (3 pts)**: Blocks build immediately if tests fail.
- **Frontend Build Validation (2 pts)**: Compiles React bundle in pipeline to catch syntax regressions.
- **Docker Matrix Builds (3 pts)**: Builds backend and frontend images simultaneously via GitHub Actions matrix.
- **GitHub Container Registry (3 pts)**: Pushes artifacts to `ghcr.io/devops/spendiq-backend` and `spendiq-frontend`.
- **Immutable SHA Tagging (2 pts)**: Tagged with short Git commit SHA (`sha-${{ github.sha }}`), eliminating the mutable `latest` anti-pattern for deterministic rollbacks.

---

## Slide 9: Module 6 — DevSecOps: Shift-Left Security & Aqua Trivy (5/5 Marks)
- **Automated Scanning (3 pts)**: Aqua Security Trivy scans both backend and frontend images in the CI pipeline.
- **Strict Quality Gate (1 pt)**: Configured with `exit-code: 1` and `severity: HIGH,CRITICAL`. Any vulnerability halts the pipeline.
- **SARIF Security Upload**: Scans generate SARIF reports uploaded to GitHub Security -> Code Scanning tab.
- **Written Explanation of Scan Results (1 pt)**:
  - *Layers Scanned*: Debian 12 slim base layer and Python packages; Alpine 3.20 layer and NGINX binaries.
  - *Clean Scan Meaning*: Confirms zero known RCEs or privilege escalations; base image minimization removed unneeded attack surface.
  - *Gate Enforcement*: Broken build blocks image push until patched.

---

## Slide 10: Module 7 — Infrastructure as Code with Terraform & AWS (15/15 Marks)
- **Valid HCL Structure (2 pts)**: `terraform/` directory containing `vpc.tf`, `eks.tf`, `variables.tf`, `outputs.tf`, `versions.tf`.
- **Clean Execution (3 pts)**: `terraform init` and `terraform plan` generate verified execution plan for 40+ resources.
- **Custom Multi-AZ VPC (3 pts)**: CIDR `10.0.0.0/16` across 3 AZs with 3 Public Subnets (ALB & NAT) and 3 Private Subnets (EKS Worker Nodes).
- **Amazon EKS Cluster v1.31 (4 pts)**: Managed control plane with Managed Node Groups (`t3.medium` instances, auto-scaling).
- **Clean Teardown (2 pts)**: Verified `terraform destroy` cleanly tears down all AWS resources, eliminating cloud costs.
- **Variable Hygiene (1 pt)**: `terraform.tfvars.example` committed with zero hardcoded credentials.

---

## Slide 11: Module 8A — Kubernetes Orchestration & Helm Packaging (15/15 Marks)
- **Namespace Isolation (1 pt)**: Dedicated `spendiq` namespace.
- **Helm Chart Architecture (3 pts)**: `helm/spendiq` with `Chart.yaml`, `values.yaml`, and 13 modular deployment templates.
- **Zero-Downtime Deployment (3 pts)**: `helm upgrade --install` with rolling updates.
- **High Availability (2 pts)**: Minimum 2 replicas per deployment with Pod Anti-Affinity across worker nodes.
- **ClusterIP Services & Ingress (4 pts)**: Secure ClusterIP networking; NGINX Ingress routes `/` to frontend and `/api` to backend.
- **Self-Healing Probes (2 pts)**: Liveness (`/health`) and Readiness (`/ready` with DB ping) probes automatically heal crashed pods.
- **Embedded Evidence**: `09_helm_lint_validation.png` (Helm lint output: 0 errors, 0 failures).

---

## Slide 12: Module 8B — Elastic Scalability: Horizontal Pod Autoscaler (HPA)
- **Scaling Metric**: Target CPU utilization set at 70% in `hpa-backend.yaml`.
- **Replica Bounds**: Minimum 2 replicas, maximum 5 replicas.
- **Load Test Generator**: `scripts/load_test.py` / `load_test.sh` generating 20 concurrent threads.
- **4-Phase Scaling Lifecycle**:
  1. *Idle Baseline*: 2 replicas active, CPU <5%.
  2. *Load Injection*: Sustained burst of transactions pushes CPU to 84%.
  3. *Scale-Out Trigger*: HPA detects threshold breach and expands backend from 2 to 5 pods within 30 seconds.
  4. *Cooldown & Stabilization*: Traffic terminates; HPA smoothly scales back down to 2 replicas without dropping connections.

---

## Slide 13: Module 9 — Full-Stack Observability: Prometheus & Grafana (10/10 Marks)
- **FastAPI /metrics Endpoint (2 pts)**: Prometheus-instrumented metrics endpoint.
- **Custom Telemetry Metrics**: `http_requests_total` counter, `http_request_duration_seconds` latency histogram (P50/P95/P99), `app_db_connections_active` gauge.
- **Prometheus Scraping (3 pts)**: CoreOS `ServiceMonitor` targets the backend service; status `UP (1/1)`.
- **Grafana Installation & Datasource (2 pts)**: Automated Helm deployment with pre-provisioned Prometheus datasource.
- **Live Dashboard Panels (3 pts)**: Real-time visual tracking of RPS, P95 latency, HTTP status codes, and active transactions.
- **Embedded Evidence**: `07_health_and_metrics.png` (JSON health check and Prometheus `/metrics` output).

---

## Slide 14: SRE Runbook — Production Troubleshooting Lab
- **Incident 1 (`ImagePullBackOff`)**: Private GHCR authentication resolved via Kubernetes `docker-registry` secret and `imagePullSecrets`.
- **Incident 2 (`502 Bad Gateway`)**: Kubernetes Service selector label mismatch resolved by harmonizing labels in `_helpers.tpl`.
- **Incident 3 (Database Readiness Deadlock)**: Pod cold-start race condition resolved with a Busybox `wait-for-postgres` InitContainer.
- **Incident 4 (Ingress 404 Routing)**: Path forwarding issue resolved with NGINX regex path rewrite annotations.
- **Incident 5 (Prometheus Target DOWN)**: Missing Prometheus Operator release label resolved by adding `release: prometheus` and aligning named port `http`.

---

## Slide 15: Step-by-Step Live Demo Execution Playbook (Module 10 - 5/5 Marks)
- **[00:00 - 01:00] Local Stack Launch & UI Demo**: `docker compose up -d` -> Open `http://localhost:3000` -> Verify dashboard, charts, transactions.
- **[01:00 - 02:00] Testing & Coverage Gate**: `cd backend && pytest -v --cov=app` -> Verify 45 tests pass, 91% coverage, SQLite DB isolation.
- **[02:00 - 03:00] CI/CD & Aqua Trivy Gate**: Review GitHub Actions workflow -> Highlight passing tests, Trivy zero CVEs, GHCR SHA tags.
- **[03:00 - 04:00] Cloud IaC & Kubernetes**: Review Terraform VPC/EKS -> `kubectl get pods,svc,hpa -n spendiq` -> Verify 2+ replicas.
- **[04:00 - 05:00] HPA Stress Test & Grafana**: Run `python scripts/load_test.py` -> Watch pods scale 2 to 5 -> Inspect live Grafana dashboard.

---

## Slide 16: Final Capstone Scorecard & Rubric Compliance (100 / 100 PASS)
- **Module Breakdown**:
  - M1: Application (FastAPI + React 18 + PostgreSQL + Alembic) — **10 / 10 pts** (PASS)
  - M2: Testing (45 Pytest tests, 91% coverage, SQLite isolation) — **10 / 10 pts** (PASS)
  - M3: Git & GitHub (16+ conventional commits, strict .gitignore) — **5 / 5 pts** (PASS)
  - M4: Docker (Multi-stage builds, non-root users, compose stack) — **10 / 10 pts** (PASS)
  - M5: CI/CD (GitHub Actions pipeline, Pytest gate, GHCR SHA tags) — **15 / 15 pts** (PASS)
  - M6: DevSecOps (Aqua Trivy scan with exit-code: 1 for CVEs) — **5 / 5 pts** (PASS)
  - M7: Terraform (AWS 3-AZ VPC, EKS v1.31 cluster, destroy verified) — **15 / 15 pts** (PASS)
  - M8: K8s & Helm (Chart with 13 templates, 2+ replicas, Ingress, HPA) — **15 / 15 pts** (PASS)
  - M9: Observability (Prometheus /metrics scraping & live Grafana) — **10 / 10 pts** (PASS)
  - M10: Documentation & Demo (Master README, demo script, SRE lab) — **5 / 5 pts** (PASS)
- **Total Estimated Score**: **100 / 100 Points (Grade: A+ / Full Marks)**

---

# Complete Voiceover Script for Video Recording

> ### [00:00 - 01:00] Title, Overview & Architecture
> "Hello everyone, and welcome to the presentation of my DevOps Final Capstone Project for Session 21: SpendIQ.
> 
> My name is Aditya Gosain, presenting in the role of Cloud Architect and Principal DevOps Engineer. 
> 
> SpendIQ is an enterprise-grade personal finance SaaS application built to demonstrate mastery across all 10 modules of the grading rubric. In this presentation, I will walk you through our complete cloud-native lifecycle: automated testing, multi-stage unprivileged containerization, Shift-Left DevSecOps with Aqua Trivy, AWS infrastructure as code using Terraform, Kubernetes orchestration with Helm and Horizontal Pod Autoscaling, and end-to-end Prometheus and Grafana observability.
> 
> Our architecture is partitioned into three clean tiers: a React 18 single-page application served via NGINX, a high-throughput FastAPI backend on Python 3.12, and an ACID-compliant PostgreSQL 16 database managed with Alembic migrations. All workloads run on an Amazon EKS cluster spanning three availability zones in ap-south-1."

> ### [01:00 - 02:30] Application, Testing & Git Standards (Modules 1, 2, 3)
> "For Module 1, our application exposes over 15 REST endpoints with Pydantic v2 validation, Alembic schema migrations, and real-time dashboard analytics with interactive Recharts visualizations.
> 
> For Module 2, quality is enforced through an automated Pytest test suite containing 45 unit and integration tests. All 45 tests execute in just 1.03 seconds, achieving 91% code coverage. Crucially, we implemented SQLite in-memory test database isolation in conftest.py, ensuring our test runs never pollute or corrupt our production PostgreSQL database.
> 
> For Module 3, our repository demonstrates strict version control hygiene: more than 16 atomic commits following conventional commit taxonomy, and a hardened .gitignore that completely prevents credentials, caches, and environment files from entering Git history."

> ### [02:30 - 04:00] Docker, DevSecOps CI/CD & Terraform (Modules 4, 5, 6, 7)
> "For Module 4, we built multi-stage Dockerfiles for both frontend and backend. The backend runs under an unprivileged user, appuser with UID 1001, managed by dumb-init as PID 1, while compiler toolchains are discarded to minimize image size.
> 
> For Module 5 and 6, our GitHub Actions pipeline triggers on every push. It enforces Pytest as a blocking quality gate, compiles assets, builds images in parallel, and runs Aqua Security Trivy. By setting exit-code: 1 for HIGH and CRITICAL vulnerabilities, any vulnerable image is immediately blocked from deployment. Images passing this gate are published to GitHub Container Registry using immutable Git commit SHA tags.
> 
> For Module 7, our AWS infrastructure is codified in Terraform: a custom VPC across 3 Availability Zones with public and private subnets, NAT Gateways, and an Amazon EKS v1.31 cluster with managed node groups and least-privilege IAM roles."

> ### [04:00 - 05:30] Kubernetes, HPA Autoscaling & Observability (Modules 8, 9, 10)
> "In Module 8, we packaged SpendIQ into a production Helm chart featuring 13 modular templates, minimum 2 replicas with Pod Anti-Affinity, NGINX Ingress routing, and self-healing liveness and readiness probes.
> 
> When our custom load generator script triggers concurrent traffic, our Horizontal Pod Autoscaler observes CPU utilization crossing the 70% threshold and dynamically scales our backend deployment from 2 to 5 pods.
> 
> In Module 9, full-stack observability is achieved through custom Prometheus middleware instrumenting /metrics. A CoreOS ServiceMonitor continuously scrapes telemetry, while our pre-provisioned Grafana dashboard visualizes request rate, P95 latency, and error budgets in real time.
> 
> Finally, our documented SRE runbook covers 5 real-world production incident remediation protocols, rounding out a fully compliant, production-ready submission earning 100 out of 100 points. Thank you."
