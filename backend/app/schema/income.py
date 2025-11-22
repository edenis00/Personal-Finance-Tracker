"""
Income schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IncomeCreate(BaseModel):
    """
    Schema for creating an income entry
    """
    amount: float
    source: str
    date: Optional[datetime] = None
    user_id: int


class IncomeUpdate(BaseModel):
    """
    Schema for updating an income entry
    """
    amount: Optional[float] = None
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

    class Config:
        orm_mode = True