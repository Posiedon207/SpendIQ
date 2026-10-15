import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST,
    CollectorRegistry, REGISTRY
)

from app.api.routes import router
from app.database import engine, Base

# ─── Prometheus Metrics ───────────────────────────────────────────────────────

REQUEST_COUNT = Counter(
    "finpilot_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "finpilot_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

ACTIVE_REQUESTS = Gauge(
    "finpilot_active_requests",
    "Number of active HTTP requests",
)

DB_CONNECTIONS = Gauge(
    "finpilot_db_connections_total",
    "Number of database connections in pool",
)

# ─── Startup / Shutdown ────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: create tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


# ─── Application Factory ──────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title="FinPilot API",
        description=(
            "Personal finance management SaaS — track transactions, "
            "manage budgets, and visualize spending analytics."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS
    allowed_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173"
    ).split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Prometheus instrumentation middleware
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        # Skip metrics endpoint itself to avoid recursion
        if request.url.path == "/metrics":
            return await call_next(request)

        ACTIVE_REQUESTS.inc()
        start_time = time.time()
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(
                time.time() - start_time
            )
            return response
        except Exception as exc:
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code="500").inc()
            raise exc
        finally:
            ACTIVE_REQUESTS.dec()

    # Include all API routes
    app.include_router(router)

    # Prometheus metrics endpoint
    @app.get("/metrics", include_in_schema=False)
    def metrics():
        """Prometheus-compatible metrics endpoint."""
        return Response(
            content=generate_latest(REGISTRY),
            media_type=CONTENT_TYPE_LATEST,
        )

    return app


app = create_app()
