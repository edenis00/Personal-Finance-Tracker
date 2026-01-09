"""
Docstring for backend.app.routes.admin
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schema.user import UserResponse, AdminUserUpdate
from app.models import User, Expense, Income, Savings
from app.dependencies.rbac import require_admin, require_permissions as require
from app.db.database import get_db
from app.utils.user import fetch_all, fetch, update, delete
from app.core.permissions import Permission
from app.schema.base import SuccessResponse


router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)


@router.get("/dashboard", response_model=SuccessResponse)
def admin_dashboard(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    logging.info(f"Admin {current_user.email} accessed the dashboard")
    """Admin dashboard endpoint"""
    total_users = db.query(User).count()
    total_expenses = db.query(Expense).count()
    total_income = db.query(Income).count()
    total_savings = db.query(Savings).count()

    logging.info(f"Dashboard stats - Users: {total_users}, Expenses: {total_expenses}, Income: {total_income}, Savings: {total_savings}")
    return SuccessResponse(
        message="Dashboard stats retrieved successfully",
        data={
            "total_users": total_users,
            "total_expenses": total_expenses,
            "total_income": total_income,
            "total_savings": total_savings,
        }
    )


@router.get("/users", response_model=SuccessResponse[list[UserResponse]])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""

    logging.info("Fetching users list by admin user_id: %s", current_user.id)
    users = fetch_all(db, skip=skip, limit=limit)

    if not users:
        logging.warning("No users found by admin user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )

    logging.info("Users list retrieved by admin user_id: %s", current_user.id)
    return SuccessResponse(
        message="Users retrieved successfully",
        data=users
    )


@router.get("/users/{user_id}", response_model=SuccessResponse[UserResponse])
def fetch_user_by_id(
    user_id: int,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get a user by ID for admins"""

    logging.info("Fetching user_id: %s by admin user_id: %s", user_id, current_user.id)
    user = fetch(db, user_id)

    if not user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User_id: %s retrieved by admin user_id: %s", user_id, current_user.id)
    return SuccessResponse(
        message="User retrieved successfully",
        data=user
    )


@router.put("/users/{user_id}", response_model=SuccessResponse[UserResponse])
def update_user_by_id(
    user_id: int,
    user: AdminUserUpdate,
    current_user: User = Depends(
        require([Permission.ADMIN_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """Update a user for admins"""

    logging.info("Updating user_id: %s by admin user_id: %s", user_id, current_user.id)
    updated_user = update(db, user, user_id)

    if not updated_user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User_id: %s updated by admin user_id: %s", user_id, current_user.id)
    return SuccessResponse(
        message="User updated successfully",
        data = updated_user
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(
        require([Permission.ADMIN_DELETE])
    ),
    db: Session = Depends(get_db)):
    """Delete a user for admins"""

    logging.info("Deleting user_id: %s by admin user_id: %s", user_id, current_user.id)
    deleted_user = delete(db, user_id)

    if not deleted_user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User_id: %s deleted by admin user_id: %s", user_id, current_user.id)
    return {"detail": "User deleted successfully"}


@router.post("/users/{user_id}", response_model=SuccessResponse[UserResponse])
def activate_deactivate_user(
    user_id: int,
    activate: bool,
    current_user: User = Depends(
        require([Permission.ADMIN_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """Activate and deactivae a user account for admins"""
    logging.info("%s user_id: %s by admin user_id: %s", "Activating" if activate else "Deactivating", user_id, current_user.id)
    user = fetch(db, user_id)
    if not user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = activate
    db.commit()
    db.refresh(user)
    logging.info("User_id: %s %s by admin user_id: %s", user_id, "activated" if activate else "deactivated", current_user.id)
    return SuccessResponse(
        message=f"User {'activated' if activate else 'deactivated'} successfully",
        data=user
    )
    

@router.get("/savings-summary", response_model=SuccessResponse)
def savings_summary(
    user_id: int|None = None,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get savings summary for all users"""

    logging.info("Fetching savings summary by admin user_id: %s", current_user.id)
    if user_id is not None:
        total_savings = db.query(Savings).filter(Savings.user_id == user_id).count()
        total_amount = db.query(Savings).with_entities(
            func.coalesce(func.sum(Savings.amount), 0)
        ).filter(Savings.user_id == user_id).scalar()
    else:

        total_savings = db.query(Savings).count()
        total_amount = db.query(Savings).with_entities(
            func.coalesce(func.sum(Savings.amount), 0)
        ).scalar()

    logging.info("Savings summary retrieved by admin user_id: %s", current_user.id)
    return SuccessResponse(
        message="Savings summary retrieved successfully",
        data={
            "total_savings": total_savings,
            "total_amount": total_amount
        }
    )


@router.get("/income-summary", response_model=SuccessResponse)
def income_summary(
    user_id: int|None = None,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get income summary for all users"""

    logging.info("Fetching income summary by admin user_id: %s", current_user.id)
    if user_id is not None:
        total_income = db.query(Income).filter(Income.user_id == user_id).count()
        total_amount = db.query(Income).with_entities(
            func.coalesce(func.sum(Income.amount), 0)
        ).filter(Income.user_id == user_id).scalar()
    else:
        total_income = db.query(Income).count()
        total_amount = db.query(Income).with_entities(
            func.coalesce(func.sum(Income.amount), 0)
        ).scalar()

    logging.info("Income summary retrieved by admin user_id: %s", current_user.id)
    return SuccessResponse(
        message="Income summary retrieved successfully",
        data={
            "total_income": total_income,
            "total_amount": total_amount
        }
    )


@router.get("/expenses-summary", response_model=SuccessResponse)
def expenses_summary(
    user_id: int|None = None,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get expenses summary for all users"""

    logging.info("Fetching expenses summary by admin user_id: %s", current_user.id)
    if user_id is not None:
        total_expenses = db.query(Expense).filter(Expense.user_id == user_id).count()
        total_amount = db.query(Expense).with_entities(
            func.coalesce(func.sum(Expense.amount), 0)
        ).filter(Expense.user_id == user_id).scalar()
    else:
        total_expenses = db.query(Expense).count()
        total_amount = db.query(Expense).with_entities(
            func.coalesce(func.sum(Expense.amount), 0)
        ).scalar()

    logging.info("Expenses summary retrieved by admin user_id: %s", current_user.id)
    return SuccessResponse(
        message="Expenses summary retrieved successfully",
        data={
            "total_expenses": total_expenses,
            "total_amount": total_amount
        }
    )