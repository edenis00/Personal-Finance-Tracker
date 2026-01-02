"""
Expense schema
"""
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal


class ExpenseCreate(BaseModel):
    """
    Schema for creating an expense entry
    """
    amount: Decimal
    category: str
    date: datetime

    @field_validator('amount')
    @classmethod
    def amount_is_positive(cls, value):
        """
        Validate that the amount is positive
        """
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator('category')
    @classmethod
    def category_not_empty(cls, value):
        """
        Validate that the category is not empty
        """
        if not value or value.strip() == "":
            raise ValueError("Category must not be empty")
        return value


class ExpenseUpdate(BaseModel):
    """
    Schema for updating an expense entry
    """
    amount: Decimal | None = None
    category: str | None = None
    date: datetime
    
    @field_validator('amount')
    @classmethod
    def amount_is_positive(cls, value):
        """
        Validate that the amount is positive
        """
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator('category')
    @classmethod
    def category_not_empty(cls, value):
        """
        Validate that the category is not empty
        """
        if not value or value.strip() == "":
            raise ValueError("Category must not be empty")
        return value


class ExpenseResponse(BaseModel):
    """
    Schema for outputting an expense entry
    """
    id: int
    amount: float
    category: str
    date: datetime
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
