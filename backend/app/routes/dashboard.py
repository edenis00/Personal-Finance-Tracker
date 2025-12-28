"""
Docstring for backend.app.routes.dashboard
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.database import get_db
from app.schema.base import SuccessResponse
from app.models import User, Expense, Income, Savings
from app.core.permissions import Permission
from app.dependencies.rbac import require_permissions


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve dashboard data
    """
    # Placeholder for actual dashboard data retrieval logic
    return {"message": "Dashboard data retrieval not yet implemented"}


@router.get("/balance", response_model=SuccessResponse)
def get_user_balance(
    current_user: User = Depends(
        require_permissions([Permission.DASHBOARD_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Get balance of a user
    """
    total_income =  db.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id
    ).scalar() or 0

    total_expense = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id
    ).scalar() or 0

    total_savings = db.query(func.sum(Savings.amount)).filter(
        Savings.user_id == current_user.id
    ).scalar() or 0

    available_balance = total_income - total_expense - total_savings
    net_balance = total_income - total_expense
    return SuccessResponse(
        message="Balance calculated successfully",
        data={
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "total_savings": float(total_savings),
            "balance": float(available_balance),
            "net_balance": float(net_balance)
        }
    )