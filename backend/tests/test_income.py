"""
Tests for income routes
"""
import pytest
from decimal import Decimal
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.models import User, Income


class TestIncomeRoutes:
    """Test cases for income routes"""

    def test_create_income_success(self, client: TestClient, test_user: User, authenticated_user_token: str, db):
        """Test successful income creation"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        income_data = {
            "amount": "2500.00",
            "source": "Salary",
        }
        response = client.post("/api/v1/incomes/", json=income_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Income created successfully"
        assert data["data"]["amount"] == "2500.00"
        assert data["data"]["source"] == "Salary"
        assert data["data"]["user_id"] == test_user.id

    def test_create_income_with_date(self, client: TestClient, test_user: User, authenticated_user_token: str, db):
        """Test creating income with custom date"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        income_date = datetime.now(timezone.utc).isoformat()
        income_data = {
            "amount": "1500.00",
            "source": "Freelance",
            "date": income_date,
        }
        response = client.post("/api/v1/incomes/", json=income_data, headers=headers)
        
        assert response.status_code == 201
        assert response.json()["data"]["source"] == "Freelance"

    def test_create_income_negative_amount(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test creating income with negative amount"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        income_data = {
            "amount": "-1000.00",
            "source": "Salary",
        }
        response = client.post("/api/v1/incomes/", json=income_data, headers=headers)
        
        assert response.status_code == 422

    def test_create_income_missing_source(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test creating income without source"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        income_data = {
            "amount": "1000.00",
        }
        response = client.post("/api/v1/incomes/", json=income_data, headers=headers)
        
        assert response.status_code == 422

    def test_create_income_without_auth(self, client: TestClient):
        """Test creating income without authentication"""
        income_data = {
            "amount": "1000.00",
            "source": "Salary",
        }
        response = client.post("/api/v1/incomes/", json=income_data)
        
        assert response.status_code == 401

    def test_read_all_incomes(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_incomes):
        """Test retrieving all incomes"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/incomes/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Incomes retrieved successfully"
        assert len(data["data"]) == 3

    def test_read_all_incomes_with_pagination(self, client: TestClient, test_user: User, authenticated_user_token: str, multiple_test_incomes):
        """Test retrieving incomes with skip and limit"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/incomes/?skip=0&limit=2", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2

    def test_read_all_incomes_empty(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test retrieving incomes when none exist"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/incomes/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    def test_read_all_incomes_without_auth(self, client: TestClient):
        """Test retrieving incomes without authentication"""
        response = client.get("/api/v1/incomes/")
        
        assert response.status_code == 401

    def test_read_income_by_id(self, client: TestClient, test_user: User, authenticated_user_token: str, test_income: Income):
        """Test retrieving a specific income"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get(f"/api/v1/incomes/{test_income.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Income retrieved successfully"
        assert data["data"]["id"] == test_income.id
        assert data["data"]["amount"] == str(test_income.amount)

    def test_read_income_not_found(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test retrieving non-existent income"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/incomes/99999", headers=headers)
        
        assert response.status_code == 404

    def test_read_income_unauthorized_user(self, client: TestClient, test_user: User, test_admin_user: User, authenticated_admin_token: str, test_income: Income):
        """Test that user cannot read another user's income"""
        headers = {"Authorization": f"Bearer {authenticated_admin_token}"}
        response = client.get(f"/api/v1/incomes/{test_income.id}", headers=headers)
        
        # Should get 404 because the income belongs to test_user, not test_admin_user
        assert response.status_code == 404

    def test_read_income_without_auth(self, client: TestClient, test_income: Income):
        """Test retrieving income without authentication"""
        response = client.get(f"/api/v1/incomes/{test_income.id}")
        
        assert response.status_code == 401

    def test_update_income_success(self, client: TestClient, test_user: User, authenticated_user_token: str, test_income: Income):
        """Test successful income update"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "amount": "3000.00",
            "source": "Salary (Updated)",
        }
        response = client.put(f"/api/v1/incomes/{test_income.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Income updated successfully"
        assert data["data"]["amount"] == "3000.00"
        assert data["data"]["source"] == "Salary (Updated)"

    def test_update_income_partial(self, client: TestClient, test_user: User, authenticated_user_token: str, test_income: Income):
        """Test partial income update"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "source": "New Source",
        }
        response = client.put(f"/api/v1/incomes/{test_income.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["source"] == "New Source"
        assert data["data"]["amount"] == str(test_income.amount)

    def test_update_income_negative_amount(self, client: TestClient, test_user: User, authenticated_user_token: str, test_income: Income):
        """Test updating income with negative amount"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "amount": "-500.00",
        }
        response = client.put(f"/api/v1/incomes/{test_income.id}", json=update_data, headers=headers)
        
        assert response.status_code == 422

    def test_update_income_not_found(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test updating non-existent income"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "amount": "2000.00",
        }
        response = client.put("/api/v1/incomes/99999", json=update_data, headers=headers)
        
        assert response.status_code == 404

    def test_update_income_unauthorized_user(self, client: TestClient, test_user: User, test_admin_user: User, authenticated_admin_token: str, test_income: Income):
        """Test that user cannot update another user's income"""
        headers = {"Authorization": f"Bearer {authenticated_admin_token}"}
        update_data = {
            "amount": "5000.00",
        }
        response = client.put(f"/api/v1/incomes/{test_income.id}", json=update_data, headers=headers)
        
        # Should fail with 401 or 404
        assert response.status_code in [401, 404]

    def test_update_income_without_auth(self, client: TestClient, test_income: Income):
        """Test updating income without authentication"""
        update_data = {
            "amount": "2000.00",
        }
        response = client.put(f"/api/v1/incomes/{test_income.id}", json=update_data)
        
        assert response.status_code == 401

    def test_delete_income_success(self, client: TestClient, test_user: User, authenticated_user_token: str, test_income: Income, db):
        """Test successful income deletion"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.delete(f"/api/v1/incomes/{test_income.id}", headers=headers)
        
        assert response.status_code == 204

    def test_delete_income_not_found(self, client: TestClient, test_user: User, authenticated_user_token: str):
        """Test deleting non-existent income"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.delete("/api/v1/incomes/99999", headers=headers)
        
        assert response.status_code == 404

    def test_delete_income_unauthorized_user(self, client: TestClient, test_user: User, test_admin_user: User, authenticated_admin_token: str, test_income: Income):
        """Test that user cannot delete another user's income"""
        headers = {"Authorization": f"Bearer {authenticated_admin_token}"}
        response = client.delete(f"/api/v1/incomes/{test_income.id}", headers=headers)
        
        # Should fail with 401 or 404
        assert response.status_code in [401, 404]

    def test_delete_income_without_auth(self, client: TestClient, test_income: Income):
        """Test deleting income without authentication"""
        response = client.delete(f"/api/v1/incomes/{test_income.id}")
        
        assert response.status_code == 401

    def test_income_isolation_between_users(self, client: TestClient, test_user: User, test_admin_user: User, authenticated_user_token: str, authenticated_admin_token: str, db):
        """Test that users can only see their own incomes"""
        # Create income for test_user
        headers_user = {"Authorization": f"Bearer {authenticated_user_token}"}
        user_income_data = {
            "amount": "2000.00",
            "source": "User Salary",
        }
        response = client.post("/api/v1/incomes/", json=user_income_data, headers=headers_user)
        assert response.status_code == 201

        # Create income for test_admin_user
        headers_admin = {"Authorization": f"Bearer {authenticated_admin_token}"}
        admin_income_data = {
            "amount": "5000.00",
            "source": "Admin Salary",
        }
        response = client.post("/api/v1/incomes/", json=admin_income_data, headers=headers_admin)
        assert response.status_code == 201

        # Test user retrieves their incomes
        response = client.get("/api/v1/incomes/", headers=headers_user)
        assert response.status_code == 200
        user_incomes = response.json()["data"]
        assert len(user_incomes) == 1
        assert all(inc["user_id"] == test_user.id for inc in user_incomes)

        # Admin retrieves their incomes
        response = client.get("/api/v1/incomes/", headers=headers_admin)
        assert response.status_code == 200
        admin_incomes = response.json()["data"]
        assert len(admin_incomes) == 1
        assert all(inc["user_id"] == test_admin_user.id for inc in admin_incomes)
