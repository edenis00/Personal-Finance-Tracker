"""
Income schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from decimal import Decimal


class IncomeCreate(BaseModel):
    """
    Schema for creating an income entry
    """
    amount: Decimal
    source: str
    date: Optional[datetime] = None

    @field_validator('amount')
    @classmethod
    def amount_is_positive(cls, value):
        """
        Validate that the amount is positive
        """
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value


class IncomeUpdate(BaseModel):
    """
    Schema for updating an income entry
    """
    amount: Optional[Decimal] = None
    source: Optional[str] = None
    date: Optional[datetime] = None


class IncomeResponse(BaseModel):
    """
    Schema for outputting an income entry
    """
    id: int
    amount: float
    source: str
    date: datetime
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
