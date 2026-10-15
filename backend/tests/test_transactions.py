"""
Tests for Transaction endpoints.
Covers: GET /api/transactions, POST /api/transactions,
        GET /api/transactions/{id}, PUT /api/transactions/{id},
        DELETE /api/transactions/{id}
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient


SAMPLE_TRANSACTION = {
    "title": "Test Salary",
    "amount": 75000.0,
    "transaction_type": "income",
    "category": "salary",
    "description": "Monthly salary payment",
    "date": "2026-10-01T00:00:00",
    "is_recurring": True,
}

SAMPLE_EXPENSE = {
    "title": "Grocery Run",
    "amount": 2500.0,
    "transaction_type": "expense",
    "category": "food",
    "description": "Weekly groceries",
    "date": "2026-10-05T00:00:00",
    "is_recurring": False,
}


class TestCreateTransaction:
    """Tests for POST /api/transactions"""

    def test_create_income_transaction(self, client: TestClient):
        """Should create an income transaction and return 201."""
        response = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == SAMPLE_TRANSACTION["title"]
        assert data["amount"] == SAMPLE_TRANSACTION["amount"]
        assert data["transaction_type"] == "income"
        assert data["id"] is not None

    def test_create_expense_transaction(self, client: TestClient):
        """Should create an expense transaction."""
        response = client.post("/api/transactions", json=SAMPLE_EXPENSE)
        assert response.status_code == 201
        data = response.json()
        assert data["transaction_type"] == "expense"
        assert data["category"] == "food"

    def test_create_transaction_with_invalid_amount(self, client: TestClient):
        """Should reject transaction with negative amount."""
        invalid = {**SAMPLE_TRANSACTION, "amount": -100.0}
        response = client.post("/api/transactions", json=invalid)
        assert response.status_code == 422  # Validation error

    def test_create_transaction_with_zero_amount(self, client: TestClient):
        """Should reject transaction with zero amount."""
        invalid = {**SAMPLE_TRANSACTION, "amount": 0.0}
        response = client.post("/api/transactions", json=invalid)
        assert response.status_code == 422

    def test_create_transaction_with_missing_title(self, client: TestClient):
        """Should reject transaction without a title."""
        invalid = {k: v for k, v in SAMPLE_TRANSACTION.items() if k != "title"}
        response = client.post("/api/transactions", json=invalid)
        assert response.status_code == 422

    def test_create_transaction_with_invalid_type(self, client: TestClient):
        """Should reject transaction with invalid type."""
        invalid = {**SAMPLE_TRANSACTION, "transaction_type": "invalid_type"}
        response = client.post("/api/transactions", json=invalid)
        assert response.status_code == 422

    def test_create_transaction_with_invalid_category(self, client: TestClient):
        """Should reject transaction with invalid category."""
        invalid = {**SAMPLE_TRANSACTION, "category": "bad_category"}
        response = client.post("/api/transactions", json=invalid)
        assert response.status_code == 422


class TestGetTransactions:
    """Tests for GET /api/transactions"""

    def test_list_transactions_empty(self, client: TestClient):
        """Should return empty list when no transactions exist."""
        response = client.get("/api/transactions")
        assert response.status_code == 200
        data = response.json()
        assert data["transactions"] == []
        assert data["total"] == 0

    def test_list_transactions_after_create(self, client: TestClient):
        """Should return created transactions."""
        client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        client.post("/api/transactions", json=SAMPLE_EXPENSE)
        response = client.get("/api/transactions")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["transactions"]) == 2

    def test_list_transactions_filter_by_type(self, client: TestClient):
        """Should filter transactions by type."""
        client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        client.post("/api/transactions", json=SAMPLE_EXPENSE)
        response = client.get("/api/transactions?transaction_type=income")
        assert response.status_code == 200
        data = response.json()
        assert all(t["transaction_type"] == "income" for t in data["transactions"])

    def test_list_transactions_pagination(self, client: TestClient):
        """Should paginate results correctly."""
        for i in range(5):
            client.post("/api/transactions", json={**SAMPLE_TRANSACTION, "title": f"Salary {i}"})
        response = client.get("/api/transactions?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["transactions"]) == 2
        assert data["total"] == 5
        assert data["total_pages"] == 3

    def test_list_transactions_search(self, client: TestClient):
        """Should filter transactions by search term."""
        client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        client.post("/api/transactions", json=SAMPLE_EXPENSE)
        response = client.get("/api/transactions?search=Salary")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["transactions"][0]["title"] == "Test Salary"


class TestGetSingleTransaction:
    """Tests for GET /api/transactions/{id}"""

    def test_get_transaction_by_id(self, client: TestClient):
        """Should return a transaction by its ID."""
        create_resp = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        tx_id = create_resp.json()["id"]
        response = client.get(f"/api/transactions/{tx_id}")
        assert response.status_code == 200
        assert response.json()["id"] == tx_id

    def test_get_nonexistent_transaction_returns_404(self, client: TestClient):
        """Should return 404 for a transaction that does not exist."""
        response = client.get("/api/transactions/99999")
        assert response.status_code == 404

    def test_get_transaction_invalid_id(self, client: TestClient):
        """Should return 422 for a non-integer ID."""
        response = client.get("/api/transactions/not-an-id")
        assert response.status_code == 422


class TestUpdateTransaction:
    """Tests for PUT /api/transactions/{id}"""

    def test_update_transaction_title(self, client: TestClient):
        """Should update a transaction's title."""
        create_resp = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        tx_id = create_resp.json()["id"]
        response = client.put(f"/api/transactions/{tx_id}", json={"title": "Updated Salary"})
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Salary"

    def test_update_transaction_amount(self, client: TestClient):
        """Should update a transaction's amount."""
        create_resp = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        tx_id = create_resp.json()["id"]
        response = client.put(f"/api/transactions/{tx_id}", json={"amount": 90000.0})
        assert response.status_code == 200
        assert response.json()["amount"] == 90000.0

    def test_update_nonexistent_transaction(self, client: TestClient):
        """Should return 404 for updating a nonexistent transaction."""
        response = client.put("/api/transactions/99999", json={"title": "Ghost"})
        assert response.status_code == 404

    def test_update_transaction_with_invalid_amount(self, client: TestClient):
        """Should reject update with negative amount."""
        create_resp = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        tx_id = create_resp.json()["id"]
        response = client.put(f"/api/transactions/{tx_id}", json={"amount": -50.0})
        assert response.status_code == 422


class TestDeleteTransaction:
    """Tests for DELETE /api/transactions/{id}"""

    def test_delete_transaction(self, client: TestClient):
        """Should delete a transaction and return 204."""
        create_resp = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        tx_id = create_resp.json()["id"]
        response = client.delete(f"/api/transactions/{tx_id}")
        assert response.status_code == 204

    def test_delete_transaction_not_found_after_delete(self, client: TestClient):
        """Deleted transaction should return 404 on subsequent GET."""
        create_resp = client.post("/api/transactions", json=SAMPLE_TRANSACTION)
        tx_id = create_resp.json()["id"]
        client.delete(f"/api/transactions/{tx_id}")
        response = client.get(f"/api/transactions/{tx_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_transaction(self, client: TestClient):
        """Should return 404 when deleting nonexistent transaction."""
        response = client.delete("/api/transactions/99999")
        assert response.status_code == 404
