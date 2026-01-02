"""
Schema models
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from decimal import Decimal


class SavingsCreate(BaseModel):
    """
    Schema for create
    """
    amount: Decimal
    current_amount: Decimal = Decimal(0.0)
    target_date: Optional[datetime] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    is_completed: bool = False

    @field_validator("amount", "current_amount")
    @classmethod
    def validate_amounts(cls, value):
        if value < 0:
            raise ValueError("Amount must be non-negative")
        return value

    @field_validator("duration_months")
    @classmethod
    def validate_duration(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Duration must be a positive integer")
        return value


class SavingsUpdate(BaseModel):
    """
    Schema for update
    """
    amount: Optional[Decimal]
    current_amount: Optional[Decimal]
    target_date: Optional[datetime]
    duration_months: Optional[int]
    description: Optional[str]
    is_completed: Optional[bool]

    @field_validator("amount", "current_amount")
    @classmethod
    def validate_amounts(cls, value):
        if value is not None and value < 0:
            raise ValueError("Amount must be non-negative")
        return value

    @field_validator("duration_months")
    @classmethod
    def validate_duration(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Duration must be a positive integer")
        return value


class SavingsResponse(BaseModel):
    """
    Schema for response
    """
    id: int
    amount: float
    current_amount: float
    target_date: Optional[datetime] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    is_completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
