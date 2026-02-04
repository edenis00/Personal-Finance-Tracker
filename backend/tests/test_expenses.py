"""
Tests for expense routes
"""
import pytest
from decimal import Decimal
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.models import User, Expense


class TestExpenseRoutes:
    """Test cases for expense routes"""

    def test_create_expense_success(self, client: TestClient, test_user: User, authenticated_user_token: str, db):
        """Test successful expense creation"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        expense_data = {
            "amount": "75.50",
            "category": "Food",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post("/api/v1/expenses/", json=expense_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Expense created successfully"
        assert data["data"]["amount"] == "75.50"
        assert data["data"]["category"] == "Food"
        assert data["data"]["user_id"] == test_user.id

    def test_create_expense_different_categories(self, client: TestClient, test_user: User, authenticated_user_token: str, db):
        """Test creating expenses in different categories"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        categories = ["Food", "Transportation", "Entertainment", "Utilities"]
        
        for category in categories:
            expense_data = {
                "amount": "50.00",
                "category": category,
                "date": datetime.now(timezone.utc).isoformat(),
            }
            response = client.post("/api/v1/expenses/", json=expense_data, headers=headers)
            assert response.status_code == 201
            assert response.json()["data"]["category"] == category

    def test_create_expense_negative_amount(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test creating expense with negative amount"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        expense_data = {
            "amount": "-50.00",
            "category": "Food",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post("/api/v1/expenses/", json=expense_data, headers=headers)
        
        assert response.status_code == 422

    def test_create_expense_empty_category(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test creating expense with empty category"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        expense_data = {
            "amount": "50.00",
            "category": "",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post("/api/v1/expenses/", json=expense_data, headers=headers)
        
        assert response.status_code == 422

    def test_create_expense_missing_fields(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test creating expense with missing required fields"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        expense_data = {
            "amount": "50.00",
            # Missing category and date
        }
        response = client.post("/api/v1/expenses/", json=expense_data, headers=headers)
        
        assert response.status_code == 422

    def test_create_expense_without_auth(self, client: TestClient):
        """Test creating expense without authentication"""
        expense_data = {
            "amount": "50.00",
            "category": "Food",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post("/api/v1/expenses/", json=expense_data)
        
        assert response.status_code == 401

    def test_read_all_expenses(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_expenses):
        """Test retrieving all expenses"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Expenses retrieved successfully"
        assert len(data["data"]) == 3

    def test_read_all_expenses_with_pagination(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_expenses):
        """Test retrieving expenses with skip and limit"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/?skip=0&limit=2", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2

    def test_read_all_expenses_empty(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test retrieving expenses when none exist"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    def test_read_all_expenses_without_auth(self, client: TestClient):
        """Test retrieving expenses without authentication"""
        response = client.get("/api/v1/expenses/")
        
        assert response.status_code == 401

    def test_read_expense_by_id(self, client: TestClient, test_user: User, authenticated_user_token: str, test_expense: Expense):
        """Test retrieving a specific expense"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get(f"/api/v1/expenses/{test_expense.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Expense retrieved successfully"
        assert data["data"]["id"] == test_expense.id
        assert data["data"]["amount"] == str(test_expense.amount)
        assert data["data"]["category"] == test_expense.category

    def test_read_expense_not_found(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test retrieving non-existent expense"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/99999", headers=headers)
        
        assert response.status_code == 404

    def test_read_expense_without_auth(self, client: TestClient, test_expense: Expense):
        """Test retrieving expense without authentication"""
        response = client.get(f"/api/v1/expenses/{test_expense.id}")
        
        assert response.status_code == 401

    def test_get_total_expenses(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_expenses):
        """Test calculating total expenses"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/total", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "total_expenses" in data
        assert data["user_id"] == test_user.id

    def test_get_total_expenses_empty(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test calculating total when no expenses exist"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/total", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_expenses"] == 0.0

    def test_get_expenses_by_category(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_expenses):
        """Test retrieving expenses by category"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/category/Food", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        assert all(exp["category"] == "Food" for exp in data["data"])

    def test_get_expenses_by_nonexistent_category(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_expenses):
        """Test retrieving expenses by non-existent category"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/expenses/category/NonExistent", headers=headers)
        
        # Should return empty list or 404 depending on implementation
        assert response.status_code in [200, 404]

    def test_update_expense_success(self, client: TestClient, test_user: User, authenticated_user_token: str, test_expense: Expense):
        """Test successful expense update"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "amount": "100.00",
            "category": "Dining",
        }
        response = client.put(f"/api/v1/expenses/{test_expense.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Expense updated successfully"
        assert data["data"]["amount"] == "100.00"
        assert data["data"]["category"] == "Dining"

    def test_update_expense_partial(self, client: TestClient, test_user: User, authenticated_user_token: str, test_expense: Expense):
        """Test partial expense update"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "category": "New Category",
        }
        response = client.put(f"/api/v1/expenses/{test_expense.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["category"] == "New Category"

    def test_update_expense_negative_amount(self, client: TestClient, test_user: User, authenticated_user_token: str, test_expense: Expense):
        """Test updating expense with negative amount"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "amount": "-50.00",
        }
        response = client.put(f"/api/v1/expenses/{test_expense.id}", json=update_data, headers=headers)
        
        assert response.status_code == 422

    def test_update_expense_not_found(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test updating non-existent expense"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "amount": "100.00",
        }
        response = client.put("/api/v1/expenses/99999", json=update_data, headers=headers)
        
        assert response.status_code == 404

    def test_update_expense_without_auth(self, client: TestClient, test_expense: Expense):
        """Test updating expense without authentication"""
        update_data = {
            "amount": "100.00",
        }
        response = client.put(f"/api/v1/expenses/{test_expense.id}", json=update_data)
        
        assert response.status_code == 401

    def test_delete_expense_success(self, client: TestClient, test_user: User, authenticated_user_token: str, test_expense: Expense, db):
        """Test successful expense deletion"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.delete(f"/api/v1/expenses/{test_expense.id}", headers=headers)
        
        assert response.status_code == 204

    def test_delete_expense_not_found(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test deleting non-existent expense"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.delete("/api/v1/expenses/99999", headers=headers)
        
        assert response.status_code == 404

    def test_delete_expense_without_auth(self, client: TestClient, test_expense: Expense):
        """Test deleting expense without authentication"""
        response = client.delete(f"/api/v1/expenses/{test_expense.id}")
        
        assert response.status_code == 401

    def test_expense_isolation_between_users(self, client: TestClient, test_user: User, test_admin_user: User, authenticated_user_token: str, authenticated_admin_token: str, db):
        """Test that users can only see their own expenses"""
        # Create expense for test_user
        headers_user = {"Authorization": f"Bearer {authenticated_user_token}"}
        user_expense_data = {
            "amount": "50.00",
            "category": "User Food",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post("/api/v1/expenses/", json=user_expense_data, headers=headers_user)
        assert response.status_code == 201

        # Create expense for test_admin_user
        headers_admin = {"Authorization": f"Bearer {authenticated_admin_token}"}
        admin_expense_data = {
            "amount": "200.00",
            "category": "Admin Food",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post("/api/v1/expenses/", json=admin_expense_data, headers=headers_admin)
        assert response.status_code == 201

        # Test user retrieves their expenses
        response = client.get("/api/v1/expenses/", headers=headers_user)
        assert response.status_code == 200
        user_expenses = response.json()["data"]
        assert len(user_expenses) == 1
        assert user_expenses[0]["user_id"] == test_user.id

        # Admin retrieves their expenses
        response = client.get("/api/v1/expenses/", headers=headers_admin)
        assert response.status_code == 200
        admin_expenses = response.json()["data"]
        assert len(admin_expenses) == 1
        assert admin_expenses[0]["user_id"] == test_admin_user.id
