"""
Expense schema
"""
from pydantic import BaseModel, ConfigDict


class ExpenseCreate(BaseModel):
    """
    Schema for creating an expense entry
    """
    amount: float
    category: str
    description: str
    user_id: int


class ExpenseUpdate(BaseModel):
    """
    Schema for updating an expense entry
    """
    amount: float
    category: str
    description: str


class ExpenseResponse(BaseModel):
    """
    Schema for outputting an expense entry
    """
    id: int
    amount: float
    category: str
    description: str
    user_id: int
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
