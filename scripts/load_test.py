#!/usr/bin/env python3
"""
FinPilot DevOps Capstone - HPA CPU Load Generator (Python)
Spikes HTTP traffic to the backend to trigger CPU utilization scaling via HPA.
"""

import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/api/transactions"
CONCURRENCY = int(sys.argv[2]) if len(sys.argv) > 2 else 20
DURATION_SECONDS = int(sys.argv[3]) if len(sys.argv) > 3 else 120


def send_requests(worker_id: int, stop_time: float) -> int:
    count = 0
    while time.time() < stop_time:
        try:
            req = urllib.request.Request(
                TARGET_URL,
                headers={"User-Agent": "FinPilot-LoadTester/1.0"}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                _ = resp.read()
                count += 1
        except Exception:
            count += 1
    return count


def main():
    print("=" * 64)
    print(" FinPilot HPA Load Generator")
    print(f" Target URL   : {TARGET_URL}")
    print(f" Concurrency  : {CONCURRENCY} threads")
    print(f" Duration     : {DURATION_SECONDS} seconds")
    print("=" * 64)
    print("Monitor HPA in another terminal:")
    print("  kubectl get hpa finpilot-backend-hpa -n finpilot -w")
    print("  kubectl get pods -n finpilot -l app.kubernetes.io/component=backend -w\n")

    start_time = time.time()
    stop_time = start_time + DURATION_SECONDS

    total_requests = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(send_requests, i, stop_time) for i in range(CONCURRENCY)]
        for f in as_completed(futures):
            total_requests += f.result()

    elapsed = time.time() - start_time
    rps = total_requests / elapsed if elapsed > 0 else 0
    print("\n" + "=" * 64)
    print(f" Completed {total_requests} requests in {elapsed:.2f}s ({rps:.2f} req/s)")
    print("=" * 64)


if __name__ == "__main__":
    main()
