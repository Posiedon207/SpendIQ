"""
Tests for Budget and Analytics endpoints.
Covers: GET /api/budgets, POST /api/budgets,
        GET /api/budgets/{id}, PUT /api/budgets/{id},
        DELETE /api/budgets/{id}, GET /api/analytics
"""
import pytest
from fastapi.testclient import TestClient


SAMPLE_BUDGET = {
    "category": "food",
    "amount": 5000.0,
    "month": 10,
    "year": 2026,
    "description": "Monthly food budget",
}

SAMPLE_TRANSACTION_INCOME = {
    "title": "Salary",
    "amount": 80000.0,
    "transaction_type": "income",
    "category": "salary",
    "date": "2026-10-01T00:00:00",
    "is_recurring": True,
}

SAMPLE_TRANSACTION_EXPENSE = {
    "title": "Rent",
    "amount": 20000.0,
    "transaction_type": "expense",
    "category": "housing",
    "date": "2026-10-01T00:00:00",
    "is_recurring": True,
}


class TestBudgetEndpoints:
    """Tests for Budget CRUD endpoints."""

    def test_create_budget(self, client: TestClient):
        """Should create a budget and return 201."""
        response = client.post("/api/budgets", json=SAMPLE_BUDGET)
        assert response.status_code == 201
        data = response.json()
        assert data["category"] == "food"
        assert data["amount"] == 5000.0
        assert data["month"] == 10
        assert data["year"] == 2026

    def test_list_budgets_empty(self, client: TestClient):
        """Should return empty list when no budgets exist."""
        response = client.get("/api/budgets")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_budgets_after_create(self, client: TestClient):
        """Should return created budgets."""
        client.post("/api/budgets", json=SAMPLE_BUDGET)
        response = client.get("/api/budgets")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_list_budgets_filter_by_month(self, client: TestClient):
        """Should filter budgets by month."""
        client.post("/api/budgets", json=SAMPLE_BUDGET)
        client.post("/api/budgets", json={**SAMPLE_BUDGET, "month": 11})
        response = client.get("/api/budgets?month=10")
        assert response.status_code == 200
        data = response.json()
        assert all(b["month"] == 10 for b in data)

    def test_get_budget_by_id(self, client: TestClient):
        """Should return a budget by its ID."""
        create_resp = client.post("/api/budgets", json=SAMPLE_BUDGET)
        budget_id = create_resp.json()["id"]
        response = client.get(f"/api/budgets/{budget_id}")
        assert response.status_code == 200
        assert response.json()["id"] == budget_id

    def test_get_nonexistent_budget(self, client: TestClient):
        """Should return 404 for a budget that does not exist."""
        response = client.get("/api/budgets/99999")
        assert response.status_code == 404

    def test_update_budget_amount(self, client: TestClient):
        """Should update budget amount."""
        create_resp = client.post("/api/budgets", json=SAMPLE_BUDGET)
        budget_id = create_resp.json()["id"]
        response = client.put(f"/api/budgets/{budget_id}", json={"amount": 7500.0})
        assert response.status_code == 200
        assert response.json()["amount"] == 7500.0

    def test_update_nonexistent_budget(self, client: TestClient):
        """Should return 404 for nonexistent budget update."""
        response = client.put("/api/budgets/99999", json={"amount": 1000.0})
        assert response.status_code == 404

    def test_delete_budget(self, client: TestClient):
        """Should delete a budget and return 204."""
        create_resp = client.post("/api/budgets", json=SAMPLE_BUDGET)
        budget_id = create_resp.json()["id"]
        response = client.delete(f"/api/budgets/{budget_id}")
        assert response.status_code == 204

    def test_delete_nonexistent_budget(self, client: TestClient):
        """Should return 404 when deleting nonexistent budget."""
        response = client.delete("/api/budgets/99999")
        assert response.status_code == 404

    def test_create_budget_invalid_month(self, client: TestClient):
        """Should reject budget with invalid month (0 or 13)."""
        invalid = {**SAMPLE_BUDGET, "month": 13}
        response = client.post("/api/budgets", json=invalid)
        assert response.status_code == 422

    def test_create_budget_invalid_amount(self, client: TestClient):
        """Should reject budget with zero or negative amount."""
        invalid = {**SAMPLE_BUDGET, "amount": 0}
        response = client.post("/api/budgets", json=invalid)
        assert response.status_code == 422


class TestAnalyticsEndpoints:
    """Tests for GET /api/analytics"""

    def test_analytics_empty_returns_zero_summary(self, client: TestClient):
        """Analytics with no transactions should return zero values."""
        response = client.get("/api/analytics")
        assert response.status_code == 200
        data = response.json()
        assert data["summary"]["total_income"] == 0.0
        assert data["summary"]["total_expenses"] == 0.0
        assert data["summary"]["net_balance"] == 0.0
        assert data["summary"]["transaction_count"] == 0

    def test_analytics_calculates_correct_summary(self, client: TestClient):
        """Analytics should correctly sum income and expenses."""
        client.post("/api/transactions", json=SAMPLE_TRANSACTION_INCOME)
        client.post("/api/transactions", json=SAMPLE_TRANSACTION_EXPENSE)
        response = client.get("/api/analytics")
        assert response.status_code == 200
        data = response.json()
        assert data["summary"]["total_income"] == 80000.0
        assert data["summary"]["total_expenses"] == 20000.0
        assert data["summary"]["net_balance"] == 60000.0
        assert data["summary"]["transaction_count"] == 2

    def test_analytics_category_breakdown(self, client: TestClient):
        """Analytics should include expense category breakdown."""
        client.post("/api/transactions", json=SAMPLE_TRANSACTION_EXPENSE)
        response = client.get("/api/analytics")
        assert response.status_code == 200
        data = response.json()
        assert len(data["expense_by_category"]) >= 1
        housing = next(c for c in data["expense_by_category"] if c["category"] == "housing")
        assert housing["total"] == 20000.0
        assert housing["percentage"] == 100.0

    def test_analytics_monthly_trend(self, client: TestClient):
        """Analytics should include monthly trend data."""
        client.post("/api/transactions", json=SAMPLE_TRANSACTION_INCOME)
        response = client.get("/api/analytics")
        assert response.status_code == 200
        data = response.json()
        assert len(data["monthly_trend"]) >= 1

    def test_analytics_has_required_fields(self, client: TestClient):
        """Analytics response should have all required fields."""
        response = client.get("/api/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "expense_by_category" in data
        assert "income_by_category" in data
        assert "monthly_trend" in data
