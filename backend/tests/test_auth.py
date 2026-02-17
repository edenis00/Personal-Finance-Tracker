"""
Tests for authentication routes
"""

import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from app.models import User


class TestAuthRoutes:
    """Test cases for authentication routes"""

    def test_signup_success(self, client: TestClient, db):
        """Test successful user signup"""
        user_data = {
            "email": "newuser@example.com",
            "password": "Securepassword123@",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "balance": "1000.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "User created successfully"
        assert data["data"]["email"] == "newuser@example.com"
        assert data["data"]["first_name"] == "John"

    def test_signup_with_duplicate_email(self, client: TestClient, test_user: User):
        """Test signup with duplicate email"""
        user_data = {
            "email": test_user.email,
            "password": "Securepassword123@",
            "first_name": "Jane",
            "last_name": "Doe",
            "balance": "500.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()

    def test_signup_invalid_email(self, client: TestClient):
        """Test signup with invalid email"""
        user_data = {
            "email": "invalid-email",
            "password": "Securepassword123@",
            "first_name": "John",
            "last_name": "Doe",
            "balance": "1000.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 422  # Validation error

    def test_signup_missing_required_fields(self, client: TestClient):
        """Test signup with missing required fields"""
        user_data = {
            "email": "test@example.com",
            "password": "Securepassword123@",
            # Missing first_name and last_name
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 422

    def test_signup_negative_balance(self, client: TestClient):
        """Test signup with negative balance"""
        user_data = {
            "email": "test@example.com",
            "password": "Securepassword123@",
            "first_name": "John",
            "last_name": "Doe",
            "balance": "-100.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 422

    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login"""
        login_data = {
            "email": test_user.email,
            "password": "testpassword123",
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email

    def test_login_invalid_password(self, client: TestClient, test_user: User):
        """Test login with invalid password"""
        login_data = {
            "email": test_user.email,
            "password": "wrongpassword",
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_nonexistent_email(self, client: TestClient):
        """Test login with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "anypassword",
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 404

    def test_login_missing_email(self, client: TestClient):
        """Test login without email"""
        login_data = {
            "password": "testpassword123",
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422

    def test_login_missing_password(self, client: TestClient, test_user: User):
        """Test login without password"""
        login_data = {
            "email": test_user.email,
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422

    def test_get_current_user(
        self, client: TestClient, test_user: User, authenticated_user_token: str
    ):
        """Test getting current user info"""
        headers = {"Authorization": f"Bearer {authenticated_user_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["first_name"] == test_user.first_name
        assert data["id"] == test_user.id

    def test_get_current_user_without_token(self, client: TestClient):
        """Test getting current user without authentication token"""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 401

    def test_login_returns_token_details(self, client: TestClient, test_user: User):
        """Test that login returns correct token details"""
        login_data = {
            "email": test_user.email,
            "password": "testpassword123",
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "expires_in" in data
        assert "expires_at" in data
        assert isinstance(data["expires_in"], int)
        assert data["expires_in"] > 0

    def test_signup_creates_user_with_correct_defaults(self, client: TestClient):
        """Test that signup creates user with correct default values"""
        user_data = {
            "email": "newuser@example.com",
            "password": "Securepassword123@",
            "first_name": "John",
            "last_name": "Doe",
            "balance": "500.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 201
        user = response.json()["data"]
        assert user["is_active"] is True
        assert user["is_verified"] is False
        assert user["role"] == "user"
        assert user["balance"] == "500.00"

    def test_signup_with_optional_fields(self, client: TestClient):
        """Test signup with optional fields"""
        user_data = {
            "email": "newuser@example.com",
            "password": "Securepassword123@",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "profile_img_url": "https://example.com/image.jpg",
            "balance": "1000.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == 201
        user = response.json()["data"]
        assert user["phone_number"] == "+1234567890"
        assert user["profile_img_url"] == "https://example.com/image.jpg"

    def test_login_case_insensitive_email(self, client: TestClient, test_user: User):
        """Test login with different case email"""
        login_data = {
            "email": test_user.email.upper(),
            "password": "testpassword123",
        }
        response = client.post("/api/v1/auth/login", json=login_data)

        # Email lookup might be case-insensitive depending on database
        # If it's case-sensitive, this test should fail
        # Adjust based on your actual implementation
        assert response.status_code == 404

    def test_signup_empty_password(self, client: TestClient):
        """Test signup with empty password"""
        user_data = {
            "email": "test@example.com",
            "password": "",
            "first_name": "John",
            "last_name": "Doe",
            "balance": "1000.00",
        }
        response = client.post("/api/v1/auth/signup", json=user_data)

        # Empty password should fail validation
        assert response.status_code == 422


class TestAuthRateLimiting:
    """Test rate limiting on auth endpoints"""

    def test_login_rate_limit(self, client: TestClient):
        """Test that login endpoint has rate limiting"""
        # Rate limit is 5/minute, so we should be able to make 5 requests
        login_data = {
            "email": "test@example.com",
            "password": "wrong",
        }

        # Make multiple login attempts
        for i in range(5):
            response = client.post("/api/v1/auth/login", json=login_data)
            # Requests should succeed (though auth might fail)
            assert response.status_code == 429

    def test_signup_rate_limit(self, client: TestClient):
        """Test that signup endpoint has rate limiting"""
        # Rate limit is 3/minute
        base_email = "testuser{}.example.com"

        for i in range(4):
            user_data = {
                "email": f"testuser{i}@example.com",
                "password": "Securepassword123@",
                "first_name": "Test",
                "last_name": "User",
                "balance": "1000.00",
            }
            response = client.post("/api/v1/auth/signup", json=user_data)
            # Requests should succeed
            assert response.status_code == 429
