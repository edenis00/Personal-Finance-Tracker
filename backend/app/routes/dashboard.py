"""
Docstring for backend.app.routes.dashboard
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.database import get_db
from app.schema.base import SuccessResponse
from app.models import User, Expense, Income
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
    total_income =  db.query(Expense)