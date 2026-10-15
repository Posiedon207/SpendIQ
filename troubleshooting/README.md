# FinPilot Production Troubleshooting Lab (Phase 10)

This guide documents five real-world Kubernetes and DevOps operational failure scenarios, providing root-cause analyses, diagnostic commands, and remediation procedures.

---

## Scenario 1: ImagePullBackOff (Invalid Image Reference or Registry Auth)

### 1. Initial Symptoms
Pod stays in `ImagePullBackOff` or `ErrImagePull` state.
```bash
kubectl get pods -n finpilot
# Output:
# NAME                                READY   STATUS             RESTARTS   AGE
# finpilot-backend-6789abc-xyz        0/1     ImagePullBackOff   0          2m
```

### 2. Diagnostic Commands
```bash
kubectl describe pod finpilot-backend-6789abc-xyz -n finpilot
kubectl get events -n finpilot --field-selector reason=Failed
```

### 3. Expected Observations
In the `Events` section:
```
Failed to pull image "ghcr.io/devops/finpilot-backend:invalid-tag": rpc error: code = NotFound desc = failed to pull and unpack image ...: not found
Warning  Failed     Failed to pull image ...
Warning  Failed     Error: ErrImagePull
Normal   BackOff    Back-off pulling image ...
Warning  Failed     Error: ImagePullBackOff
```

### 4. Root Cause
1. Typo in image tag or repository URI in `values.yaml` or Deployment manifest.
2. Missing GHCR image-pull secret (`imagePullSecrets`) if the repository is private.

### 5. Corrective Action
Update the image reference to a verified digest or tag:
```bash
# Correcting via Helm upgrade:
helm upgrade finpilot ./helm/finpilot -n finpilot \
  --set backend.image.tag="1.0.0"

# Or if private GHCR, create imagePullSecret:
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<GITHUB_USER> \
  --docker-password=<GH_PAT_TOKEN> \
  -n finpilot
```

### 6. Verification
```bash
kubectl rollout status deployment/finpilot-backend -n finpilot
# Output: deployment "finpilot-backend" successfully rolled out
```

---

## Scenario 2: Service Selector Mismatch (Endpoints Not Found)

### 2. Initial Symptoms
Traffic to frontend or backend times out with HTTP 502/504 or "no endpoints available".

### 2. Diagnostic Commands
```bash
kubectl get endpoints finpilot-backend -n finpilot
kubectl get svc finpilot-backend -n finpilot -o yaml | grep -A 3 selector
kubectl get pods -n finpilot --show-labels
```

### 3. Expected Observations
The Service `Endpoints` field is `<none>`:
```
NAME               ENDPOINTS   AGE
finpilot-backend   <none>      5m
```

### 4. Root Cause
The `spec.selector` in `backend-service.yaml` does not match the Pod labels defined in `spec.template.metadata.labels` in `backend-deployment.yaml`.
For example, Service specifies `app: finpilot-backend` while Deployment pods have `app.kubernetes.io/component: backend`.

### 5. Corrective Action
Align the selectors in the Service manifest:
```yaml
spec:
  selector:
    app.kubernetes.io/component: backend
    app.kubernetes.io/name: finpilot
```
Apply the updated chart:
```bash
helm upgrade finpilot ./helm/finpilot -n finpilot
```

### 6. Verification
```bash
kubectl get endpoints finpilot-backend -n finpilot
# Output:
# NAME               ENDPOINTS                                   AGE
# finpilot-backend   10.244.1.15:8000,10.244.2.19:8000           6m
```

---

## Scenario 3: Application Failing Readiness Probe (Database Unreachable)

### 1. Initial Symptoms
Pods are in `Running` status but never reach `READY 1/1` (shows `READY 0/1`). Traffic is not routed to the Pod.
```bash
kubectl get pods -n finpilot
# NAME                                READY   STATUS    RESTARTS   AGE
# finpilot-backend-78bdf4c89-2klmp    0/1     Running   0          3m
```

### 2. Diagnostic Commands
```bash
kubectl describe pod finpilot-backend-78bdf4c89-2klmp -n finpilot
kubectl logs finpilot-backend-78bdf4c89-2klmp -n finpilot
curl -i http://<POD_IP>:8000/ready
```

### 3. Expected Observations
In the describe output:
```
Warning  Unhealthy  Readiness probe failed: HTTP probe failed with statuscode: 503
```
In backend application logs:
```
sqlalchemy.exc.OperationalError: could not connect to server: Connection refused
```

### 4. Root Cause
1. PostgreSQL service name is misspelled in `DATABASE_URL` (e.g. `localhost` instead of `finpilot-postgres`).
2. PostgreSQL pod crashed or is restarting due to disk quota/permissions.
3. Secret `finpilot-postgres-secret` has invalid credentials.

### 5. Corrective Action
1. Check PostgreSQL pod status and logs:
   ```bash
   kubectl get pods -l app.kubernetes.io/component=database -n finpilot
   kubectl logs -l app.kubernetes.io/component=database -n finpilot
   ```
2. Verify `DATABASE_URL` secret:
   ```bash
   kubectl get secret finpilot-postgres-secret -n finpilot -o jsonpath="{.data.DATABASE_URL}" | base64 -d
   ```
3. Ensure PostgreSQL is ready before backend probes trigger (verified by our `wait-for-postgres` initContainer).

### 6. Verification
```bash
kubectl get pods -n finpilot -l app.kubernetes.io/component=backend
# Output: 1/1 Running
```

---

## Scenario 4: Ingress Path Routing or 404/502 Gateway Errors

### 1. Initial Symptoms
Accessing `http://finpilot.local/api/transactions` returns `404 Not Found` or `502 Bad Gateway`.

### 2. Diagnostic Commands
```bash
kubectl describe ingress finpilot-ingress -n finpilot
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=50
curl -v -H "Host: finpilot.local" http://<INGRESS_CONTROLLER_IP>/api/transactions
```

### 3. Expected Observations
Ingress access log shows:
```
"GET /api/transactions HTTP/1.1" 404
```
Backend log shows request arrived with unexpected prefix or missing URI segment.

### 4. Root Cause
Missing or incorrect regex rewrite annotation in NGINX Ingress Controller. In NGINX ingress:
`path: /api(/|$)(.*)` requires `nginx.ingress.kubernetes.io/rewrite-target: /$2` so that `/api/transactions` is forwarded to the backend as `/api/transactions`.

### 5. Corrective Action
Update `helm/finpilot/templates/ingress.yaml` to include appropriate rewrite annotations or pass unmodified URLs directly.
```yaml
annotations:
  nginx.ingress.kubernetes.io/use-regex: "true"
  nginx.ingress.kubernetes.io/rewrite-target: /api/$2
```
Or route directly if FastAPI handles `/api` route prefix (which FinPilot does in `app/api/routes.py`).

### 6. Verification
```bash
curl -H "Host: finpilot.local" http://<INGRESS_IP>/api/transactions
# Output: {"transactions":[],"total":0,"page":1,"page_size":20,"total_pages":0}
```

---

## Scenario 5: Prometheus Target DOWN (Scrape Failure)

### 1. Initial Symptoms
In the Prometheus UI (`/targets`), target `finpilot-backend` is listed with state `DOWN`.
In Grafana, metric panels show `No data`.

### 2. Diagnostic Commands
```bash
# Check if Prometheus can reach the backend metrics endpoint
kubectl port-forward svc/finpilot-backend 8000:8000 -n finpilot &
curl -s http://localhost:8000/metrics | head -n 10

# Check ServiceMonitor selector
kubectl get servicemonitor -n finpilot -o yaml

# Inspect Prometheus logs
kubectl logs -l app.kubernetes.io/name=prometheus -n monitoring --tail=100 | grep -i "scrape"
```

### 3. Expected Observations
Prometheus Targets page shows:
`Get "http://10.244.1.15:8000/metrics": context deadline exceeded` or `connection refused` or target missing entirely.

### 4. Root Cause
1. Target port mismatch: Service defines port `8000` named `http`, but ServiceMonitor references port `metrics` instead of `http`.
2. NetworkPolicy blocking traffic between `monitoring` namespace and `finpilot` namespace.
3. Prometheus server missing permissions to scrape outside its namespace.

### 5. Corrective Action
Align the port name in `ServiceMonitor` to match `finpilot-backend` service:
```yaml
endpoints:
  - port: http
    path: /metrics
    interval: 15s
```
Verify label matching between Prometheus CRD selector (`release: prometheus`) and ServiceMonitor label.

### 6. Verification
Navigate to Prometheus Web UI -> **Status** -> **Targets**:
Target `finpilot-backend-monitor` reports state **UP (1/1)**.
Execute PromQL query in Prometheus:
`finpilot_http_requests_total` returns live counters.
