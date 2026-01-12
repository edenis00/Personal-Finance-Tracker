"""
Test configuration and fixtures for the Personal Finance Tracker backend
"""

import pytest
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app
from app.models import User, Income, Expense, Savings
from app.schema.user import UserCreate
from app.utils.auth import hash_password
from fastapi.testclient import TestClient


# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override the get_db dependency to use the test database"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Provide a test client for making requests to the app"""
    # Ensure tables exist before each test
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Clean up after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a clean database for each test"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db: Session):
    """Create a test user"""
    hashed_password = hash_password("testpassword123")
    user = User(
        email="testuser@example.com",
        password=hashed_password,
        first_name="Test",
        last_name="User",
        phone_number="+1234567890",
        role="user",
        balance=Decimal("1000.00"),
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_admin_user(db: Session):
    """Create a test admin user"""
    hashed_password = hash_password("adminpassword123")
    admin = User(
        email="admin@example.com",
        password=hashed_password,
        first_name="Admin",
        last_name="User",
        phone_number="+1987654321",
        role="admin",
        balance=Decimal("5000.00"),
        is_active=True,
        is_verified=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def test_income(db: Session, test_user: User):
    """Create a test income entry"""
    income = Income(
        amount=Decimal("2500.00"),
        source="Salary",
        user_id=test_user.id,
        date=datetime.now(timezone.utc),
    )
    db.add(income)
    test_user.balance += income.amount
    db.commit()
    db.refresh(income)
    db.refresh(test_user)
    return income


@pytest.fixture(scope="function")
def test_expense(db: Session, test_user: User):
    """Create a test expense entry"""
    expense = Expense(
        amount=Decimal("150.50"),
        category="Food",
        user_id=test_user.id,
        date=datetime.now(timezone.utc),
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@pytest.fixture(scope="function")
def test_savings(db: Session, test_user: User):
    """Create a test savings entry"""
    savings = Savings(
        user_id=test_user.id,
        amount=Decimal("5000.00"),
        current_amount=Decimal("2000.00"),
        duration_months=12,
        description="Vacation Fund",
        is_completed=False,
    )
    db.add(savings)
    db.commit()
    db.refresh(savings)
    return savings


@pytest.fixture(scope="function")
def multiple_test_incomes(db: Session, test_user: User):
    """Create multiple test income entries"""
    incomes = [
        Income(
            amount=Decimal("2500.00"),
            source="Salary",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        ),
        Income(
            amount=Decimal("500.00"),
            source="Freelance",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        ),
        Income(
            amount=Decimal("100.00"),
            source="Bonus",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        ),
    ]
    db.add_all(incomes)
    for income in incomes:
        test_user.balance += income.amount
    db.commit()
    for income in incomes:
        db.refresh(income)
    db.refresh(test_user)
    return incomes


@pytest.fixture(scope="function")
def multiple_test_expenses(db: Session, test_user: User):
    """Create multiple test expense entries"""
    expenses = [
        Expense(
            amount=Decimal("50.00"),
            category="Food",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        ),
        Expense(
            amount=Decimal("100.00"),
            category="Transportation",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        ),
        Expense(
            amount=Decimal("75.50"),
            category="Entertainment",
            user_id=test_user.id,
            date=datetime.now(timezone.utc),
        ),
    ]
    db.add_all(expenses)
    db.commit()
    for expense in expenses:
        db.refresh(expense)
    return expenses


@pytest.fixture(scope="function")
def authenticated_user_token(test_user: User, client: TestClient):
    """Get an authentication token for the test user"""
    from app.utils.auth import create_access_token

    token, _ = create_access_token(data={"user_id": str(test_user.id)})
    return token


@pytest.fixture(scope="function")
def authenticated_admin_token(test_admin_user: User, client: TestClient):
    """Get an authentication token for the admin user"""
    from app.utils.auth import create_access_token

    token, _ = create_access_token(data={"user_id": str(test_admin_user.id)})
    return token
