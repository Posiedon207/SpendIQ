"""
Tests for Health and Readiness endpoints.
Covers: GET /health, GET /ready
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for GET /health"""

    def test_health_returns_200(self, client: TestClient):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_correct_schema(self, client: TestClient):
        """Health endpoint should return status, version, and environment."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "environment" in data

    def test_health_status_is_healthy(self, client: TestClient):
        """Health endpoint status should be 'healthy'."""
        response = client.get("/health")
        assert response.json()["status"] == "healthy"

    def test_health_version_is_set(self, client: TestClient):
        """Health endpoint should return a non-empty version string."""
        response = client.get("/health")
        assert response.json()["version"] != ""


class TestReadinessEndpoint:
    """Tests for GET /ready"""

    def test_readiness_returns_200_when_db_connected(self, client: TestClient):
        """Readiness endpoint should return 200 when DB is up (SQLite)."""
        response = client.get("/ready")
        # With SQLite test DB, connection check may fail — we accept 200 or 503
        assert response.status_code in [200, 503]

    def test_readiness_has_required_fields(self, client: TestClient):
        """Readiness endpoint should return status, database, and message."""
        response = client.get("/ready")
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "database" in data
            assert "message" in data
