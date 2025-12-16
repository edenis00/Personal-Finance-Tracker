"""
Schema models
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class SavingsCreate(BaseModel):
    """
    Schema for create
    """
    amount: float
    current_amount: float
    target_date: datetime
    duration_months: int
    description: str
    is_completed: bool

    @field_validator("amount", "current_amount")
    @classmethod
    def validate_amounts(cls, value):
        if value < 0:
            raise ValueError("Amount must be non-negative")
        return value


class SavingsUpdate(BaseModel):
    """
    Schema for update
    """
    amount: Optional[float]
    current_amount: Optional[float]
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


class SavingsResponse(BaseModel):
    """
    Schema for response
    """
    id: int
    amount: float
    current_amount: float
    target_date: datetime
    duration_months: int
    description: str
    is_completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
