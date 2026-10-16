# SpendIQ Production Troubleshooting & SRE Runbook Lab

This runbook documents 5 critical production failure scenarios encountered during cloud-native Kubernetes deployment, their root causes, diagnostic procedures, and battle-tested remediation steps.

---

## Incident 1: `ImagePullBackOff` & GHCR Secret Authentication

### Symptoms
- Pods remain in `ImagePullBackOff` or `ErrImagePull` state.
- `kubectl describe pod <backend-pod-name> -n spendiq` displays:
  ```
  Failed to pull image "ghcr.io/devops/spendiq-backend:sha-abcdef1": rpc error: code = Unknown desc = failed to pull and unpack image: failed to resolve reference: unexpected status from HEAD request to https://ghcr.io/v2/devops/spendiq-backend/manifests/sha-abcdef1: 401 Unauthorized
  ```

### Root Cause
GitHub Container Registry (GHCR) packages are private by default. The Kubernetes cluster does not possess valid image pull credentials to authenticate against GHCR.

### Remediation Procedure
1. Generate a GitHub Personal Access Token (PAT) with `read:packages` scope.
2. Create a Kubernetes `docker-registry` secret in the `spendiq` namespace:
   ```bash
   kubectl create secret docker-registry ghcr-secret \
     --namespace spendiq \
     --docker-server=ghcr.io \
     --docker-username=<GITHUB_USERNAME> \
     --docker-password=<GITHUB_PAT> \
     --docker-email=<EMAIL>
   ```
3. Attach the secret to the deployment or ServiceAccount in `helm/spendiq/values.yaml`:
   ```yaml
   imagePullSecrets:
     - name: ghcr-secret
   ```
4. Verify pods pull the image successfully:
   ```bash
   kubectl get pods -n spendiq -w
   ```

---

## Incident 2: Kubernetes Service Selector Mismatch (502 Bad Gateway)

### Symptoms
- Ingress returns `502 Bad Gateway` when querying `/api/health`.
- `kubectl get endpoints spendiq-backend -n spendiq` displays `<none>`.

### Root Cause
The Service selector labels defined in `service-backend.yaml` did not match the pod labels in `deployment-backend.yaml` (e.g. `app.kubernetes.io/name: spendiq-backend` vs `app: backend`). As a result, the Service failed to associate any pod endpoints.

### Remediation Procedure
1. Inspect the running pod labels:
   ```bash
   kubectl get pods -n spendiq --show-labels
   ```
2. Inspect the service selector:
   ```bash
   kubectl get svc spendiq-backend -n spendiq -o yaml | grep -A 3 selector
   ```
3. Harmonize selector labels in Helm chart templates (`helm/spendiq/templates/_helpers.tpl` and `service-backend.yaml`):
   ```yaml
   spec:
     selector:
       app.kubernetes.io/name: spendiq-backend
       app.kubernetes.io/instance: spendiq
   ```
4. Apply the updated Helm release:
   ```bash
   helm upgrade spendiq ./helm/spendiq -n spendiq
   kubectl get endpoints spendiq-backend -n spendiq
   ```

---

## Incident 3: Database Readiness Deadlock & Migration Race Condition

### Symptoms
- Backend pods enter `CrashLoopBackOff` upon initial cluster deployment.
- Pod logs show:
  ```
  sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server: Connection refused
  Is the server running on host "spendiq-postgres" and accepting TCP/IP connections on port 5432?
  ```

### Root Cause
FastAPI backend pods attempted to run Alembic database migrations immediately on startup before the PostgreSQL StatefulSet had completed its initial database initialization and storage mounting.

### Remediation Procedure
1. Add an `initContainer` in `helm/spendiq/templates/deployment-backend.yaml` that polls PostgreSQL until it is accepting connections:
   ```yaml
   initContainers:
     - name: wait-for-postgres
       image: busybox:1.36
       command: ['sh', '-c', 'until nc -z -v -w3 spendiq-postgres 5432; do echo "Waiting for PostgreSQL..."; sleep 2; done;']
   ```
2. Configure readiness probe on PostgreSQL:
   ```yaml
   readinessProbe:
     exec:
       command: ["pg_isready", "-U", "spendiq", "-d", "spendiq"]
     initialDelaySeconds: 5
     periodSeconds: 5
   ```
3. Backend pods now deterministically wait for PostgreSQL to become fully ready before executing `alembic upgrade head`.

---

## Incident 4: Ingress Path Routing & NGINX Rewrite Conflicts

### Symptoms
- Requests to `http://<INGRESS_IP>/` succeed and load the React SPA.
- Requests to `http://<INGRESS_IP>/api/transactions` return `404 Not Found` or NGINX default error page.

### Root Cause
NGINX Ingress was forwarding the prefix `/api` directly to FastAPI without stripping or properly rewriting the URI, or the FastAPI route was configured without the prefix.

### Remediation Procedure
1. In `helm/spendiq/templates/ingress.yaml`, ensure proper annotations are configured:
   ```yaml
   metadata:
     annotations:
       kubernetes.io/ingress.class: nginx
       nginx.ingress.kubernetes.io/use-regex: "true"
   spec:
     rules:
       - http:
           paths:
             - path: /api(/|$)(.*)
               pathType: ImplementationSpecific
               backend:
                 service:
                   name: spendiq-backend
                   port:
                     number: 8000
             - path: /(.*)
               pathType: ImplementationSpecific
               backend:
                 service:
                   name: spendiq-frontend
                   port:
                     number: 3000
   ```
2. Verify route resolution via curl:
   ```bash
   curl -I http://<INGRESS_IP>/api/health
   # HTTP/1.1 200 OK
   ```

---

## Incident 5: Prometheus ServiceMonitor Target Scraping Failure (Target DOWN)

### Symptoms
- Prometheus UI -> Status -> Targets displays `spendiq-backend` as `DOWN (0/1)` or target does not appear at all.
- Grafana dashboard panels show "No Data".

### Root Cause
The `ServiceMonitor` resource in `helm/spendiq/templates/servicemonitor.yaml` was missing the Prometheus operator's release label (e.g. `release: prometheus`), causing the Prometheus operator to ignore the resource. Additionally, the backend service port name did not match the port specified in `ServiceMonitor.spec.endpoints[0].port`.

### Remediation Procedure
1. Check Prometheus operator target label selectors:
   ```bash
   kubectl get prometheus -n monitoring -o yaml | grep -A 5 serviceMonitorSelector
   ```
2. Update `servicemonitor.yaml` labels to match:
   ```yaml
   metadata:
     name: spendiq-backend-monitor
     namespace: spendiq
     labels:
       release: prometheus
   spec:
     selector:
       matchLabels:
         app.kubernetes.io/name: spendiq-backend
     endpoints:
       - port: http
         path: /metrics
         interval: 15s
   ```
3. In `service-backend.yaml`, verify the port is named:
   ```yaml
   ports:
     - name: http
       port: 8000
       targetPort: 8000
   ```
4. Verify target appears in Prometheus UI under Targets with status `UP (1/1)`.
