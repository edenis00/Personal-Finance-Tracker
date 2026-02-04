"""
Tests for utility functions
"""

import pytest
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models import User
from app.schema.user import UserCreate, UserUpdate
from app.utils.auth import (
    hash_password,
    verify_password,
    is_password_strong,
    validate_password,
    create_access_token,
    decode_access_token,
)
from app.services.user_service import (
    get_user_service,
    get_all_users_service,
    get_user_by_email_service,
    create_user_service,
    update_user_service,
    delete_user_service,
)


class TestAuthUtils:
    """Test cases for authentication utilities"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "securepassword123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "securepassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "securepassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_is_password_strong_valid(self):
        """Test strong password validation with valid password"""
        strong_password = "StrongPass123!"
        assert is_password_strong(strong_password) is True

    def test_is_password_strong_too_short(self):
        """Test password validation with too short password"""
        weak_password = "Pass1!"
        with pytest.raises(ValueError) as exc_info:
            is_password_strong(weak_password)
        assert "at least 8 characters" in str(exc_info.value)

    def test_is_password_strong_no_uppercase(self):
        """Test password validation without uppercase letter"""
        weak_password = "weakpass123!"
        with pytest.raises(ValueError) as exc_info:
            is_password_strong(weak_password)
        assert "uppercase" in str(exc_info.value).lower()

    def test_is_password_strong_no_lowercase(self):
        """Test password validation without lowercase letter"""
        weak_password = "WEAKPASS123!"
        with pytest.raises(ValueError) as exc_info:
            is_password_strong(weak_password)
        assert "lowercase" in str(exc_info.value).lower()

    def test_is_password_strong_no_digit(self):
        """Test password validation without digit"""
        weak_password = "WeakPass!"
        with pytest.raises(ValueError) as exc_info:
            is_password_strong(weak_password)
        assert "digit" in str(exc_info.value).lower()

    def test_is_password_strong_no_special_char(self):
        """Test password validation without special character"""
        weak_password = "WeakPass123"
        with pytest.raises(ValueError) as exc_info:
            is_password_strong(weak_password)
        assert "special character" in str(exc_info.value).lower()

    def test_validate_password_valid(self):
        """Test validate_password with strong password"""
        strong_password = "StrongPass123!"
        # Should not raise exception
        validate_password(strong_password)

    def test_validate_password_invalid(self):
        """Test validate_password with weak password"""
        weak_password = "weak"
        with pytest.raises(ValueError):
            validate_password(weak_password)

    def test_create_access_token(self):
        """Test JWT token creation"""
        user_data = {"user_id": "123"}
        token, expire = create_access_token(user_data)

        assert token is not None
        assert len(token) > 0
        assert expire is not None

    def test_decode_access_token_valid(self):
        """Test decoding a valid token"""
        user_id = "123"
        token, _ = create_access_token({"user_id": user_id})

        payload = decode_access_token(token)
        assert payload["sub"] == user_id

    def test_decode_access_token_invalid(self):
        """Test decoding an invalid token"""
        invalid_token = "invalid.token.here"

        with pytest.raises(Exception):
            decode_access_token(invalid_token)

    def test_token_contains_user_id(self):
        """Test that token contains user ID"""
        user_id = "456"
        token, _ = create_access_token({"user_id": user_id})

        payload = decode_access_token(token)
        assert payload["sub"] == user_id

    def test_token_contains_expiry(self):
        """Test that token contains expiry information"""
        token, _ = create_access_token({"user_id": "789"})
        payload = decode_access_token(token)

        assert "exp" in payload
        assert "iat" in payload

    def test_hash_same_password_different_hashes(self):
        """Test that same password produces different hashes"""
        password = "MyPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)


class TestUserUtils:
    """Test cases for user utilities"""

    def test_fetch_user_by_id(self, db: Session, test_user: User):
        """Test fetching user by ID"""
        fetched_user = get_user_service(db, test_user.id)

        assert fetched_user is not None
        assert fetched_user.id == test_user.id
        assert fetched_user.email == test_user.email

    def test_fetch_user_not_found(self, db: Session):
        """Test fetching non-existent user"""
        fetched_user = get_user_service(db, 99999)

        assert fetched_user is None

    def test_fetch_all_users(self, db: Session, test_user: User, test_admin_user: User):
        """Test fetching all users"""
        users = get_all_users_service(db)

        assert len(users) >= 2
        user_ids = [u.id for u in users]
        assert test_user.id in user_ids
        assert test_admin_user.id in user_ids

    def test_fetch_all_users_with_pagination(self, db: Session, test_user: User):
        """Test fetching users with pagination"""
        users = get_all_users_service(db, skip=0, limit=1)

        assert len(users) == 1

    def test_fetch_by_email(self, db: Session, test_user: User):
        """Test fetching user by email"""
        fetched_user = get_user_by_email_service(db, test_user.email)

        assert fetched_user is not None
        assert fetched_user.email == test_user.email
        assert fetched_user.id == test_user.id

    def test_fetch_by_email_not_found(self, db: Session):
        """Test fetching user by non-existent email"""
        fetched_user = get_user_by_email_service(db, "nonexistent@example.com")

        assert fetched_user is None

    def test_create_user(self, db: Session):
        """Test creating a new user"""
        user_data = UserCreate(
            email="newuser@example.com",
            password="NewPass123!",
            first_name="New",
            last_name="User",
            balance=Decimal("500.00"),
        )

        new_user = create_user_service(db, user_data)

        assert new_user.id is not None
        assert new_user.email == "newuser@example.com"
        assert new_user.first_name == "New"
        assert verify_password("NewPass123!", new_user.password)

    def test_create_user_duplicate_email(self, db: Session, test_user: User):
        """Test creating user with duplicate email"""
        user_data = UserCreate(
            email=test_user.email,
            password="NewPass123!",
            first_name="Duplicate",
            last_name="User",
            balance=Decimal("500.00"),
        )

        with pytest.raises(ValueError) as exc_info:
            create_user_service(db, user_data)
        assert "already registered" in str(exc_info.value).lower()

    def test_update_user_email(self, db: Session, test_user: User):
        """Test updating user email"""
        update_data = UserUpdate(email="newemail@example.com")

        updated_user = update_user_service(db, update_data, test_user.id)

        assert updated_user is not None
        assert updated_user.email == "newemail@example.com"
        assert updated_user.first_name == test_user.first_name

    def test_update_user_password(self, db: Session, test_user: User):
        """Test updating user password"""
        new_password = "NewPassword123!"
        update_data = UserUpdate(password=new_password)

        updated_user = update_user_service(db, update_data, test_user.id)

        assert updated_user is not None
        assert verify_password(new_password, updated_user.password)

    def test_update_user_multiple_fields(self, db: Session, test_user: User):
        """Test updating multiple user fields"""
        update_data = UserUpdate(
            first_name="Updated",
            last_name="Name",
            phone_number="+9876543210",
        )

        updated_user = update_user_service(db, update_data, test_user.id)

        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.phone_number == "+9876543210"

    def test_update_user_not_found(self, db: Session):
        """Test updating non-existent user"""
        update_data = UserUpdate(first_name="Updated")

        result = update_user_service(db, update_data, 99999)

        assert result is None

    def test_update_user_partial(self, db: Session, test_user: User):
        """Test partial user update (only updates provided fields)"""
        original_email = test_user.email
        update_data = UserUpdate(first_name="ChangedName")

        updated_user = update_user_service(db, update_data, test_user.id)

        assert updated_user.first_name == "ChangedName"
        assert updated_user.email == original_email

    def test_delete_user(self, db: Session, test_user: User):
        """Test deleting a user"""
        user_id = test_user.id
        deleted_user = delete_user_service(db, user_id)

        assert deleted_user is not None
        assert deleted_user.id == user_id

        # Verify user is deleted
        fetched_user = get_user_service(db, user_id)
        assert fetched_user is None

    def test_delete_user_not_found(self, db: Session):
        """Test deleting non-existent user"""
        result = delete_user_service(db, 99999)

        assert result is None

    def test_create_user_with_no_password(self, db: Session):
        """Test creating user without password"""
        user_data = UserCreate(
            email="nopass@example.com",
            password="",  # Empty password
            first_name="No",
            last_name="Pass",
            balance=Decimal("100.00"),
        )

        # Should handle empty password appropriately
        # Should raise validation error or be handled by schema
        # Since we enforce password strength, this should fail at schema validation level
        # This test is updated to catch the ValidationError
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            UserCreate(
                email="nopass@example.com",
                password="",  # Empty password
                first_name="No",
                last_name="Pass",
                balance=Decimal("100.00"),
            )

    def test_fetch_all_users_limit(self, db: Session):
        """Test fetching limited number of users"""
        users = get_all_users_service(db, skip=0, limit=1)

        assert len(users) <= 1

    def test_create_user_hashes_password(self, db: Session):
        """Test that user password is hashed during creation"""
        plain_password = "PlainPassword123!"
        user_data = UserCreate(
            email="hashtest@example.com",
            password=plain_password,
            first_name="Hash",
            last_name="Test",
            balance=Decimal("100.00"),
        )

        new_user = create_user_service(db, user_data)

        # Password should not be plain text
        assert new_user.password != plain_password
        # But should verify correctly
        assert verify_password(plain_password, new_user.password)
