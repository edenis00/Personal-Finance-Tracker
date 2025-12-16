"""
Schema models
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


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
