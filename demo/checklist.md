# FinPilot Live Demo Execution Checklist

Follow this command sequence during the live video evaluation or presentation.

---

## 1. Local Stack Demonstration (Docker Compose)
```bash
# Verify configuration
docker compose config

# Spin up complete stack
docker compose up -d --build

# Verify all containers are healthy (frontend, backend, db)
docker compose ps

# Seed sample financial data
curl -X POST http://localhost:8000/api/seed

# Test health and readiness endpoints
curl -s http://localhost:8000/health | jq
curl -s http://localhost:8000/ready | jq

# Open Browser: http://localhost:3000
# - Verify dashboard stats, graphs, and transaction list
# - Add a new transaction
# - Add a budget

# Shut down local stack
docker compose down -v
```

---

## 2. Automated Testing & Code Quality
```bash
cd backend
# Execute Pytest test suite with code coverage
pytest --tb=short -v --cov=app --cov-report=term-missing
cd ..
```

---

## 3. GitHub Actions CI/CD & DevSecOps Verification
1. Navigate to GitHub Repository -> **Actions** tab.
2. Demonstrate the latest workflow run on `main`:
   - Point out **Backend Tests (Pytest)** passing.
   - Point out **Frontend Build Validation** passing.
   - Point out **Trivy Security Scan** for both frontend and backend images.
   - Point out images pushed to **GitHub Container Registry (GHCR)**.

---

## 4. Terraform AWS Infrastructure
```bash
cd terraform

# Validate syntax
terraform validate

# Inspect plan
terraform plan -var-file="terraform.tfvars.example"

# Display outputs (if already applied)
terraform output
cd ..
```

---

## 5. Kubernetes & Helm Deployment
```bash
# Connect to EKS cluster
aws eks update-kubeconfig --region ap-south-1 --name finpilot-eks

# Verify nodes
kubectl get nodes -o wide

# Verify Helm chart installation
helm list -n finpilot

# Verify all Pods, Services, PVC, and Ingress
kubectl get pods,svc,pvc,ingress -n finpilot -o wide

# Confirm both backend and frontend have at least 2 replicas running
```

---

## 6. HPA Autoscaling Live Test
```bash
# Open Terminal 1: Watch HPA and Pods
kubectl get hpa finpilot-backend-hpa -n finpilot -w

# Open Terminal 2: Run load generator
python scripts/load_test.py http://<INGRESS_OR_LB_IP>/api/transactions 25 120

# Observe HPA: Targets CPU% climbs from <5% to >80%
# Observe Pods: Replicas scale up from 2 to 3, 4, 5
```

---

## 7. Prometheus & Grafana Observability
```bash
# Forward Grafana port
kubectl port-forward svc/grafana 3000:80 -n monitoring

# Open Browser: http://localhost:3000
# Login: admin / finpilot_grafana_admin_password
# Open Dashboard: "FinPilot - Production Observability Dashboard"
# Highlight:
#  - Active Request Rate
#  - P95 Latency graph responding to load test
#  - Status code breakdown (200 OK)
#  - Target status in Prometheus UI (UP 1/1)
```
