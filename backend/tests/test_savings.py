"""
Tests for savings routes
"""

import pytest
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.models import User, Savings


class TestSavingsRoutes:
    """Test cases for savings routes"""

    def test_create_savings_success(
        self, client: TestClient, test_user: User, authenticated_user_token: str, db
    ):
        """Test successful savings creation"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        savings_data = {
            "amount": "5000.00",
            "current_amount": "2000.00",
            "duration_months": 12,
            "description": "Vacation Fund",
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Savings created successfully"
        assert data["data"]["amount"] == "5000.00"
        assert data["data"]["current_amount"] == "2000.00"
        assert data["data"]["user_id"] == test_user.id

    def test_create_savings_minimal_data(
        self, client: TestClient, test_user: User, authenticated_user_token: str, db
    ):
        """Test creating savings with minimal data"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        savings_data = {
            "amount": "1000.00",
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["amount"] == "1000.00"
        assert data["data"]["user_id"] == test_user.id

    def test_create_savings_with_target_date(
        self, client: TestClient, test_user: User, authenticated_user_token: str, db
    ):
        """Test creating savings with target date"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        target_date = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
        savings_data = {
            "amount": "10000.00",
            "target_date": target_date,
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)

        assert response.status_code == 201

    def test_create_savings_negative_amount(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test creating savings with negative amount"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        savings_data = {
            "amount": "-1000.00",
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)

        assert response.status_code == 422

    def test_create_savings_invalid_duration(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test creating savings with invalid duration"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        savings_data = {
            "amount": "1000.00",
            "duration_months": -6,
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)

        assert response.status_code == 422

    def test_create_savings_without_auth(self, client: TestClient):
        """Test creating savings without authentication"""
        savings_data = {
            "amount": "1000.00",
        }
        response = client.post("/api/v1/savings/", json=savings_data)

        assert response.status_code == 401

    def test_read_savings_by_id(
        self,
        client: TestClient,
        test_user: User,
        authenticated_user_token: str,
        test_savings: Savings,
    ):
        """Test retrieving a specific savings entry"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get(f"/api/v1/savings/{test_savings.id}", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Savings retrieved successfully"
        assert data["data"]["id"] == test_savings.id
        assert data["data"]["user_id"] == test_user.id

    def test_read_savings_not_found(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test retrieving non-existent savings"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/savings/99999", headers=headers)

        assert response.status_code == 404

    def test_read_savings_without_auth(self, client: TestClient, test_savings: Savings):
        """Test retrieving savings without authentication"""
        response = client.get(f"/api/v1/savings/{test_savings.id}")

        assert response.status_code == 401

    def test_read_all_savings_for_user(
        self, client: TestClient, test_user: User, authenticated_user_token: str, db
    ):
        """Test retrieving all savings for a user"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}

        # Create multiple savings
        for i in range(3):
            savings = Savings(
                user_id=test_user.id,
                amount="1000.00",
                description=f"Goal {i+1}",
            )
            db.add(savings)
        db.commit()

        response = client.get("/api/v1/savings/", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Savings retrieved successfully"
        assert len(data["data"]) == 3

    def test_read_all_savings_empty(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test retrieving all savings when none exist"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/savings/", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    def test_read_all_savings_without_auth(self, client: TestClient):
        """Test retrieving all savings without authentication"""
        response = client.get("/api/v1/savings/")

        assert response.status_code == 401

    def test_update_savings_success(
        self,
        client: TestClient,
        test_user: User,
        authenticated_user_token: str,
        test_savings: Savings,
    ):
        """Test successful savings update"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "current_amount": "3500.00",
            "description": "Updated Vacation Fund",
        }
        response = client.put(
            f"/api/v1/savings/{test_savings.id}", json=update_data, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Savings updated successfully"
        assert data["data"]["current_amount"] == "3500.00"
        assert data["data"]["description"] == "Updated Vacation Fund"

    def test_update_savings_mark_completed(
        self,
        client: TestClient,
        test_user: User,
        authenticated_user_token: str,
        test_savings: Savings,
    ):
        """Test marking savings as completed"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "current_amount": test_savings.amount,
            "is_completed": True,
        }
        response = client.put(
            f"/api/v1/savings/{test_savings.id}", json=update_data, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_completed"] is True

    def test_update_savings_partial(
        self,
        client: TestClient,
        test_user: User,
        authenticated_user_token: str,
        test_savings: Savings,
    ):
        """Test partial savings update"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "description": "New Description",
        }
        response = client.put(
            f"/api/v1/savings/{test_savings.id}", json=update_data, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["description"] == "New Description"

    def test_update_savings_negative_amount(
        self,
        client: TestClient,
        test_user: User,
        authenticated_user_token: str,
        test_savings: Savings,
    ):
        """Test updating savings with negative amount"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "current_amount": "-100.00",
        }
        response = client.put(
            f"/api/v1/savings/{test_savings.id}", json=update_data, headers=headers
        )

        assert response.status_code == 422

    def test_update_savings_not_found(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test updating non-existent savings"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        update_data = {
            "description": "Updated",
        }
        response = client.put(
            "/api/v1/savings/99999", json=update_data, headers=headers
        )

        assert response.status_code == 404

    def test_update_savings_without_auth(
        self, client: TestClient, test_savings: Savings
    ):
        """Test updating savings without authentication"""
        update_data = {
            "description": "Updated",
        }
        response = client.put(f"/api/v1/savings/{test_savings.id}", json=update_data)

        assert response.status_code == 401

    def test_delete_savings_success(
        self,
        client: TestClient,
        test_user: User,
        authenticated_user_token: str,
        test_savings: Savings,
        db,
    ):
        """Test successful savings deletion"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.delete(f"/api/v1/savings/{test_savings.id}", headers=headers)

        assert response.status_code == 204

    def test_delete_savings_not_found(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test deleting non-existent savings"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.delete("/api/v1/savings/99999", headers=headers)

        assert response.status_code == 404

    def test_delete_savings_without_auth(
        self, client: TestClient, test_savings: Savings
    ):
        """Test deleting savings without authentication"""
        response = client.delete(f"/api/v1/savings/{test_savings.id}")

        assert response.status_code == 401

    def test_savings_isolation_between_users(
        self,
        client: TestClient,
        test_user: User,
        test_admin_user: User,
        authenticated_user_token: str,
        authenticated_admin_token: str,
        db,
    ):
        """Test that users can only see their own savings"""
        # Create savings for test_user
        headers_user = {"Authorization": f"Bearer {authenticated_user_token}"}
        user_savings_data = {
            "amount": "1000.00",
            "description": "User Goal",
        }
        response = client.post(
            "/api/v1/savings/", json=user_savings_data, headers=headers_user
        )
        assert response.status_code == 201

        # Create savings for test_admin_user
        headers_admin = {"Authorization": f"Bearer {authenticated_admin_token}"}
        admin_savings_data = {
            "amount": "5000.00",
            "description": "Admin Goal",
        }
        response = client.post(
            "/api/v1/savings/", json=admin_savings_data, headers=headers_admin
        )
        assert response.status_code == 201

        # Test user retrieves their savings
        response = client.get("/api/v1/savings/", headers=headers_user)
        assert response.status_code == 200
        user_savings = response.json()["data"]
        assert len(user_savings) == 1
        assert user_savings[0]["user_id"] == test_user.id

        # Admin retrieves all savings (admin can see all)
        response = client.get("/api/v1/savings/", headers=headers_admin)
        assert response.status_code == 200
        admin_view = response.json()["data"]
        # Admin should be able to see all savings or only their own depending on implementation
        assert len(admin_view) >= 1

    def test_savings_with_all_fields(
        self, client: TestClient, test_user: User, authenticated_user_token: str, db
    ):
        """Test creating savings with all fields"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        target_date = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
        savings_data = {
            "amount": "10000.00",
            "current_amount": "5000.00",
            "target_date": target_date,
            "duration_months": 24,
            "description": "House down payment",
            "is_completed": False,
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["amount"] == "10000.00"
        assert data["data"]["current_amount"] == "5000.00"
        assert data["data"]["duration_months"] == 24
        assert data["data"]["description"] == "House down payment"
        assert data["data"]["is_completed"] is False

    def test_update_progress_towards_goal(
        self, client: TestClient, test_user: User, authenticated_user_token: str, db
    ):
        """Test updating progress towards a savings goal"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}

        # Create savings goal
        savings_data = {
            "amount": "1000.00",
            "current_amount": "0.00",
        }
        response = client.post("/api/v1/savings/", json=savings_data, headers=headers)
        savings_id = response.json()["data"]["id"]

        # Update progress
        updates = [
            "100.00",
            "250.00",
            "500.00",
            "1000.00",
        ]

        for amount in updates:
            update_data = {"current_amount": amount}
            response = client.put(
                f"/api/v1/savings/{savings_id}", json=update_data, headers=headers
            )
            assert response.status_code == 200
            assert response.json()["data"]["current_amount"] == str(amount)
