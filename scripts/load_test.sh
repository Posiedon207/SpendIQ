#!/usr/bin/env bash
# ==============================================================================
# SpendIQ DevOps Capstone - HPA CPU Load Generator
# Spikes traffic to the SpendIQ backend to demonstrate Horizontal Pod Autoscaler (HPA)
# ==============================================================================

TARGET_URL="${1:-http://localhost:8000/api/transactions}"
CONCURRENCY="${2:-20}"
DURATION_SECONDS="${3:-180}"

echo "=================================================================="
echo " Starting HPA CPU Load Test for SpendIQ Backend"
echo " Target URL   : ${TARGET_URL}"
echo " Concurrency  : ${CONCURRENCY} workers"
echo " Duration     : ${DURATION_SECONDS} seconds"
echo "=================================================================="
echo ""
echo "Tip: In another terminal, watch HPA in action:"
echo "  kubectl get hpa spendiq-backend-hpa -n spendiq -w"
echo "  kubectl get pods -n spendiq -l app.kubernetes.io/component=backend -w"
echo ""

START_TIME=$(date +%s)
END_TIME=$((START_TIME + DURATION_SECONDS))

# Function for a single load worker
run_worker() {
  local worker_id=$1
  local requests=0
  while [ $(date +%s) -lt $END_TIME ]; do
    # Heavy analytical queries or transaction requests
    curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}" > /dev/null 2>&1
    requests=$((requests + 1))
  done
  echo "Worker ${worker_id} completed ${requests} requests."
}

# Spawn concurrent background workers
PIDS=()
for i in $(seq 1 $CONCURRENCY); do
  run_worker "$i" &
  PIDS+=($!)
done

echo "Spawned ${CONCURRENCY} workers generating CPU load..."

# Wait for all workers to finish
for pid in "${PIDS[@]}"; do
  wait "$pid"
done

TOTAL_TIME=$(( $(date +%s) - START_TIME ))
echo ""
echo "=================================================================="
echo " Load test completed in ${TOTAL_TIME} seconds."
echo " Verify HPA scale-down (takes ~5 minutes stabilization window):"
echo "   kubectl get hpa spendiq-backend-hpa -n spendiq"
echo "=================================================================="
