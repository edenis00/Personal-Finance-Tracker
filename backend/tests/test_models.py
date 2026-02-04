"""
Tests for database models
"""
import pytest
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models import User, Income, Expense, Savings
from app.utils.auth import hash_password


class TestUserModel:
    """Test cases for the User model"""

    def test_create_user(self, db: Session):
        """Test creating a user"""
        user = User(
            email="test@example.com",
            password=hash_password("password123"),
            first_name="John",
            last_name="Doe",
            phone_number="+1234567890",
            role="user",
            balance=Decimal("1000.00"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.balance == Decimal("1000.00")
        assert user.is_active is True
        assert user.role == "user"

    def test_user_default_values(self, db: Session):
        """Test that user has correct default values"""
        user = User(
            email="default@example.com",
            password=hash_password("password123"),
            first_name="Jane",
            last_name="Smith",
            balance=Decimal("500.00"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.balance == Decimal("500.00")
        assert user.is_active is True
        assert user.is_verified is False
        assert user.role == "user"
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_relationships(self, db: Session, test_user: User, test_income: Income, test_expense: Expense):
        """Test user relationships with income and expenses"""
        user = db.query(User).filter(User.id == test_user.id).first()
        assert user is not None
        assert len(user.incomes) > 0
        assert len(user.expenses) > 0

    def test_user_str_representation(self, test_user: User):
        """Test user string representation"""
        user_str = str(test_user)
        assert "User" in user_str
        assert str(test_user.id) in user_str
        assert test_user.email in user_str

    def test_unique_email_constraint(self, db: Session, test_user: User):
        """Test that email must be unique"""
        duplicate_user = User(
            email=test_user.email,
            password=hash_password("password123"),
            first_name="Duplicate",
            last_name="User",
            balance=Decimal("100.00"),
        )
        db.add(duplicate_user)
        with pytest.raises(Exception):
            db.commit()

    def test_unique_phone_number_constraint(self, db: Session, test_user: User):
        """Test that phone number must be unique"""
        if test_user.phone_number:
            duplicate_user = User(
                email="different@example.com",
                password=hash_password("password123"),
                first_name="Another",
                last_name="User",
                phone_number=test_user.phone_number,
                balance=Decimal("100.00"),
            )
            db.add(duplicate_user)
            with pytest.raises(Exception):
                db.commit()


class TestIncomeModel:
    """Test cases for the Income model"""

    def test_create_income(self, db: Session, test_user: User):
        """Test creating an income entry"""
        income = Income(
            amount=Decimal("2500.00"),
            source="Salary",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        )
        db.add(income)
        db.commit()
        db.refresh(income)

        assert income.id is not None
        assert income.amount == Decimal("2500.00")
        assert income.source == "Salary"
        assert income.user_id == test_user.id
        assert income.created_at is not None

    def test_income_user_relationship(self, db: Session, test_income: Income, test_user: User):
        """Test income relationship with user"""
        income = db.query(Income).filter(Income.id == test_income.id).first()
        assert income is not None
        assert income.user_id == test_user.id
        assert income.user.email == test_user.email

    def test_income_cascade_delete(self, db: Session, test_user: User):
        """Test that deleting a user deletes their incomes"""
        income = Income(
            amount=Decimal("1500.00"),
            source="Freelance",
            user_id=test_user.id,
        )
        db.add(income)
        db.commit()
        income_id = income.id

        db.delete(test_user)
        db.commit()

        deleted_income = db.query(Income).filter(Income.id == income_id).first()
        assert deleted_income is None

    def test_income_str_representation(self, test_income: Income):
        """Test income string representation"""
        income_str = str(test_income)
        assert "Income" in income_str
        assert str(test_income.id) in income_str
        assert str(test_income.amount) in income_str

    def test_multiple_incomes_for_user(self, db: Session, test_user: User):
        """Test creating multiple incomes for one user"""
        incomes_data = [
            {"amount": Decimal("2500.00"), "source": "Salary"},
            {"amount": Decimal("500.00"), "source": "Freelance"},
            {"amount": Decimal("100.00"), "source": "Interest"},
        ]

        for data in incomes_data:
            income = Income(
                amount=data["amount"],
                source=data["source"],
                user_id=test_user.id,
            )
            db.add(income)
        db.commit()

        user_incomes = db.query(Income).filter(Income.user_id == test_user.id).all()
        assert len(user_incomes) == 3


class TestExpenseModel:
    """Test cases for the Expense model"""

    def test_create_expense(self, db: Session, test_user: User):
        """Test creating an expense entry"""
        expense = Expense(
            amount=Decimal("75.50"),
            category="Food",
            user_id=test_user.id,
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)

        assert expense.id is not None
        assert expense.amount == Decimal("75.50")
        assert expense.category == "Food"
        assert expense.user_id == test_user.id
        assert expense.created_at is not None

    def test_expense_user_relationship(self, db: Session, test_expense: Expense, test_user: User):
        """Test expense relationship with user"""
        expense = db.query(Expense).filter(Expense.id == test_expense.id).first()
        assert expense is not None
        assert expense.user_id == test_user.id
        assert expense.user.email == test_user.email

    def test_expense_cascade_delete(self, db: Session, test_user: User):
        """Test that deleting a user deletes their expenses"""
        expense = Expense(
            amount=Decimal("100.00"),
            category="Entertainment",
            user_id=test_user.id,
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

        db.delete(test_user)
        db.commit()

        deleted_expense = db.query(Expense).filter(Expense.id == expense_id).first()
        assert deleted_expense is None

    def test_expense_str_representation(self, test_expense: Expense):
        """Test expense string representation"""
        expense_str = str(test_expense)
        assert "Expense" in expense_str
        assert str(test_expense.id) in expense_str
        assert str(test_expense.amount) in expense_str

    def test_multiple_expenses_for_user(self, db: Session, test_user: User):
        """Test creating multiple expenses for one user"""
        categories = ["Food", "Transportation", "Entertainment", "Utilities"]
        for category in categories:
            expense = Expense(
                amount=Decimal("50.00"),
                category=category,
                user_id=test_user.id,
            )
            db.add(expense)
        db.commit()

        user_expenses = db.query(Expense).filter(Expense.user_id == test_user.id).all()
        assert len(user_expenses) == 4


class TestSavingsModel:
    """Test cases for the Savings model"""

    def test_create_savings(self, db: Session, test_user: User):
        """Test creating a savings entry"""
        savings = Savings(
            user_id=test_user.id,
            amount=Decimal("5000.00"),
            current_amount=Decimal("2000.00"),
            duration_months=12,
            description="Vacation Fund",
        )
        db.add(savings)
        db.commit()
        db.refresh(savings)

        assert savings.id is not None
        assert savings.amount == Decimal("5000.00")
        assert savings.current_amount == Decimal("2000.00")
        assert savings.duration_months == 12
        assert savings.is_completed is False

    def test_savings_default_values(self, db: Session, test_user: User):
        """Test savings default values"""
        savings = Savings(
            user_id=test_user.id,
            amount=Decimal("1000.00"),
        )
        db.add(savings)
        db.commit()
        db.refresh(savings)

        assert savings.is_completed is False
        assert savings.created_at is not None
        assert savings.updated_at is not None

    def test_savings_user_relationship(self, db: Session, test_savings: Savings, test_user: User):
        """Test savings relationship with user"""
        savings = db.query(Savings).filter(Savings.id == test_savings.id).first()
        assert savings is not None
        assert savings.user_id == test_user.id
        assert savings.user.email == test_user.email

    def test_savings_cascade_delete(self, db: Session, test_user: User):
        """Test that deleting a user deletes their savings"""
        savings = Savings(
            user_id=test_user.id,
            amount=Decimal("3000.00"),
            description="Emergency Fund",
        )
        db.add(savings)
        db.commit()
        savings_id = savings.id

        db.delete(test_user)
        db.commit()

        deleted_savings = db.query(Savings).filter(Savings.id == savings_id).first()
        assert deleted_savings is None

    def test_mark_savings_as_completed(self, db: Session, test_savings: Savings):
        """Test marking a savings goal as completed"""
        test_savings.is_completed = True
        test_savings.current_amount = test_savings.amount
        db.commit()
        db.refresh(test_savings)

        assert test_savings.is_completed is True
        assert test_savings.current_amount == test_savings.amount

    def test_update_savings_amount(self, db: Session, test_savings: Savings):
        """Test updating savings amount"""
        original_amount = test_savings.current_amount
        test_savings.current_amount = Decimal("3000.00")
        db.commit()
        db.refresh(test_savings)

        assert test_savings.current_amount != original_amount
        assert test_savings.current_amount == Decimal("3000.00")
