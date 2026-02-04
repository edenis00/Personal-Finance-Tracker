"""
Tests for Pydantic schemas
"""
import pytest
from decimal import Decimal
from datetime import datetime, timezone
from pydantic import ValidationError

from app.schema.user import UserCreate, UserUpdate, UserRole
from app.schema.income import IncomeCreate, IncomeUpdate, IncomeResponse
from app.schema.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.schema.savings import SavingsCreate, SavingsUpdate, SavingsResponse


class TestUserSchema:
    """Test cases for User schemas"""

    def test_valid_user_create(self):
        """Test creating a valid UserCreate schema"""
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "role": UserRole.USER,
            "balance": Decimal("1000.00"),
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.balance == Decimal("1000.00")

    def test_invalid_email_format(self):
        """Test that invalid email raises validation error"""
        user_data = {
            "email": "invalid-email",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
            "balance": Decimal("1000.00"),
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_negative_balance(self):
        """Test that negative balance raises validation error"""
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
            "balance": Decimal("-100.00"),
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_update_partial(self):
        """Test UserUpdate with partial data"""
        update_data = {
            "email": "newemail@example.com",
            "first_name": "Jane",
        }
        user_update = UserUpdate(**update_data)
        assert user_update.email == "newemail@example.com"
        assert user_update.first_name == "Jane"
        assert user_update.last_name is None

    def test_user_role_enum(self):
        """Test UserRole enum values"""
        assert UserRole.USER.value == "user"
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.MODERATOR.value == "moderator"


class TestIncomeSchema:
    """Test cases for Income schemas"""

    def test_valid_income_create(self):
        """Test creating a valid IncomeCreate schema"""
        income_data = {
            "amount": Decimal("2500.00"),
            "source": "Salary",
        }
        income = IncomeCreate(**income_data)
        assert income.amount == Decimal("2500.00")
        assert income.source == "Salary"

    def test_income_amount_must_be_positive(self):
        """Test that income amount must be positive"""
        income_data = {
            "amount": Decimal("-100.00"),
            "source": "Salary",
        }
        with pytest.raises(ValidationError) as exc_info:
            IncomeCreate(**income_data)
        assert "Amount must be positive" in str(exc_info.value)

    def test_income_amount_cannot_be_zero(self):
        """Test that income amount cannot be zero"""
        income_data = {
            "amount": Decimal("0.00"),
            "source": "Salary",
        }
        with pytest.raises(ValidationError):
            IncomeCreate(**income_data)

    def test_income_create_with_date(self):
        """Test creating income with date"""
        now = datetime.now(timezone.utc)
        income_data = {
            "amount": Decimal("1000.00"),
            "source": "Freelance",
            "date": now,
        }
        income = IncomeCreate(**income_data)
        assert income.date == now

    def test_income_update(self):
        """Test IncomeUpdate schema"""
        update_data = {
            "amount": Decimal("3000.00"),
        }
        update = IncomeUpdate(**update_data)
        assert update.amount == Decimal("3000.00")
        assert update.source is None

    def test_income_response_model(self):
        """Test IncomeResponse schema"""
        now = datetime.now(timezone.utc)
        response_data = {
            "id": 1,
            "amount": Decimal("2500.00"),
            "source": "Salary",
            "date": now,
            "user_id": 1,
            "created_at": now,
            "updated_at": now,
        }
        income_response = IncomeResponse(**response_data)
        assert income_response.id == 1
        assert income_response.amount == Decimal("2500.00")


class TestExpenseSchema:
    """Test cases for Expense schemas"""

    def test_valid_expense_create(self):
        """Test creating a valid ExpenseCreate schema"""
        expense_data = {
            "amount": Decimal("75.50"),
            "category": "Food",
            "date": datetime.now(timezone.utc),
        }
        expense = ExpenseCreate(**expense_data)
        assert expense.amount == Decimal("75.50")
        assert expense.category == "Food"

    def test_expense_amount_must_be_positive(self):
        """Test that expense amount must be positive"""
        expense_data = {
            "amount": Decimal("-50.00"),
            "category": "Entertainment",
            "date": datetime.now(timezone.utc),
        }
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(**expense_data)
        assert "Amount must be positive" in str(exc_info.value)

    def test_expense_category_cannot_be_empty(self):
        """Test that category cannot be empty"""
        expense_data = {
            "amount": Decimal("50.00"),
            "category": "",
            "date": datetime.now(timezone.utc),
        }
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(**expense_data)
        assert "Category must not be empty" in str(exc_info.value)

    def test_expense_category_with_spaces_only(self):
        """Test that category with only spaces is invalid"""
        expense_data = {
            "amount": Decimal("50.00"),
            "category": "   ",
            "date": datetime.now(timezone.utc),
        }
        with pytest.raises(ValidationError):
            ExpenseCreate(**expense_data)

    def test_expense_update_partial(self):
        """Test ExpenseUpdate with partial data"""
        update_data = {
            "amount": Decimal("100.00"),
        }
        update = ExpenseUpdate(**update_data)
        assert update.amount == Decimal("100.00")
        assert update.category is None
        assert update.date is None

    def test_expense_response_model(self):
        """Test ExpenseResponse schema"""
        now = datetime.now(timezone.utc)
        response_data = {
            "id": 1,
            "amount": Decimal("75.50"),
            "category": "Food",
            "date": now,
            "user_id": 1,
            "created_at": now,
            "updated_at": now,
        }
        expense_response = ExpenseResponse(**response_data)
        assert expense_response.id == 1
        assert expense_response.category == "Food"


class TestSavingsSchema:
    """Test cases for Savings schemas"""

    def test_valid_savings_create(self):
        """Test creating a valid SavingsCreate schema"""
        savings_data = {
            "amount": Decimal("5000.00"),
            "current_amount": Decimal("2000.00"),
            "duration_months": 12,
            "description": "Vacation Fund",
        }
        savings = SavingsCreate(**savings_data)
        assert savings.amount == Decimal("5000.00")
        assert savings.current_amount == Decimal("2000.00")
        assert savings.duration_months == 12

    def test_savings_amount_cannot_be_negative(self):
        """Test that amount cannot be negative"""
        savings_data = {
            "amount": Decimal("-1000.00"),
        }
        with pytest.raises(ValidationError) as exc_info:
            SavingsCreate(**savings_data)
        assert "Amount must be non-negative" in str(exc_info.value)

    def test_savings_duration_must_be_positive(self):
        """Test that duration must be positive"""
        savings_data = {
            "amount": Decimal("1000.00"),
            "duration_months": -6,
        }
        with pytest.raises(ValidationError) as exc_info:
            SavingsCreate(**savings_data)
        assert "Duration must be a positive integer" in str(exc_info.value)

    def test_savings_duration_zero_invalid(self):
        """Test that duration of zero is invalid"""
        savings_data = {
            "amount": Decimal("1000.00"),
            "duration_months": 0,
        }
        with pytest.raises(ValidationError):
            SavingsCreate(**savings_data)

    def test_savings_create_defaults(self):
        """Test SavingsCreate default values"""
        savings_data = {
            "amount": Decimal("1000.00"),
        }
        savings = SavingsCreate(**savings_data)
        assert savings.current_amount == Decimal("0.0")
        assert savings.is_completed is False
        assert savings.duration_months is None

    def test_savings_update_partial(self):
        """Test SavingsUpdate with partial data"""
        update_data = {
            "current_amount": Decimal("3000.00"),
            "is_completed": True,
        }
        update = SavingsUpdate(**update_data)
        assert update.current_amount == Decimal("3000.00")
        assert update.is_completed is True
        assert update.amount is None

    def test_savings_response_model(self):
        """Test SavingsResponse schema"""
        now = datetime.now(timezone.utc)
        response_data = {
            "id": 1,
            "amount": Decimal("5000.00"),
            "current_amount": Decimal("2000.00"),
            "duration_months": 12,
            "description": "Vacation Fund",
            "is_completed": False,
            "user_id": 1,
            "created_at": now,
            "updated_at": now,
        }
        savings_response = SavingsResponse(**response_data)
        assert savings_response.id == 1
        assert savings_response.amount == Decimal("5000.00")
        assert savings_response.is_completed is False

    def test_savings_completion(self):
        """Test marking savings as completed"""
        response_data = {
            "id": 1,
            "amount": Decimal("1000.00"),
            "current_amount": Decimal("1000.00"),
            "is_completed": True,
            "user_id": 1,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        savings = SavingsResponse(**response_data)
        assert savings.is_completed is True
        assert savings.current_amount == savings.amount
