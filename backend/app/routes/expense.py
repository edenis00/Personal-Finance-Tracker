"""
Expense routes 
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Expense, User
from app.dependencies.auth import get_current_active_user
from app.utils.expense import calculate_total_expenses, filter_expenses_by_category, check_ownership
from app.schema.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.schema.base import SuccessResponse
from app.core.permissions import Permission, Role
from app.dependencies.rbac import require_permissions as require


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

logger = logging.getLogger(__name__)


@router.post("/", response_model=SuccessResponse[ExpenseResponse], status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(
        require(Permission.EXPENSE_WRITE)
    ),
    db: Session = Depends(get_db)):
    """
    Create a new expense entry
    """
    logging.info("Creating expense for user_id: %s, amount: %s, category: %s", current_user.id, expense.amount, expense.category)

    db_expense = Expense(**expense.model_dump(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    logger.info("Expense created with id: %s for user_id: %s", db_expense.id, current_user.id)

    return SuccessResponse(
        message="Expense created successfully",
        data=db_expense
    )


@router.get("/", response_model=SuccessResponse[list[ExpenseResponse]])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(
        require([Permission.EXPENSE_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve all expense entries for the current user
    """
    if current_user.role == Role.ADMIN.value:
        # Admin can see all expenses
        logging.info("Admin user_id: %s fetching all expenses", current_user.id)
        expenses = db.query(Expense).offset(skip).limit(limit).all()
    else:
        # Regular user can see only their own expenses
        logging.info("Fetching expenses for user_id: %s", current_user.id)
        expenses = db.query(Expense).filter(Expense.user_id == current_user.id).offset(skip).limit(limit).all()

    logging.info("Found %d expenses for user_id: %s", len(expenses), current_user.id)   
    return SuccessResponse(
        message="Expenses retrieved successfully",
        data=expenses
    )


@router.get("/total")
def get_total_expenses(
    current_user: User = Depends(
        require([Permission.EXPENSE_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Calculate total expenses for a user
    """
    logging.info("Calculating total expenses for user_id: %s", current_user.id)
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        logging.warning("No expenses found for user_id: %s", current_user.id)
        return {"user_id": current_user.id, "total_expenses": 0.0}

    total = calculate_total_expenses(expenses)

    logging.info("Total expenses for user_id: %s is %f", current_user.id, total)
    return {"user_id": current_user.id, "total_expenses": total}


@router.get("/category/{category}", response_model=SuccessResponse[list[ExpenseResponse]])
def get_expenses_by_category(
    category: str,
    current_user: User = Depends(
        require([Permission.EXPENSE_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve expenses for a user filtered by category
    """
    logging.info("Fetching expenses for user_id: %s in category: %s", current_user.id, category)
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        logging.warning("No expenses found for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expenses not found"
        )

    filtered_expenses = filter_expenses_by_category(expenses, category)
    logging.info("Found %d expenses for user_id: %s in category: %s", len(filtered_expenses), current_user.id, category)
    return SuccessResponse(
        message="Expenses retrieved successfully",
        data=filtered_expenses
    )


@router.get("/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
def read_expense(
    expense_id: int,
    current_user: User = Depends(
        require([Permission.EXPENSE_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve an expense entry by ID
    """
    logging.info("Fetching expense id: %s for user_id: %s", expense_id, current_user.id)
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        logging.warning("Expense id: %s not found for user_id: %s", expense_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    if not check_ownership(expense, current_user):
        logging.warning("Unauthorized access attempt to expense id: %s by user_id: %s", expense_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this expense"
        )

    logging.info("Expense id: %s found for user_id: %s", expense_id, current_user.id)
    return SuccessResponse(
        message="Expense retrieved successfully",
        data=expense
    )


@router.put("/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: User = Depends(
        require([Permission.EXPENSE_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """
    Update an existing expense entry
    """
    logging.info("Updating expense id: %s for user_id: %s", expense_id, current_user.id)
    expense_exists = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense_exists is None:
        logging.warning("Expense id: %s not found for user_id: %s", expense_id, current_user.id)
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if not check_ownership(expense_exists, current_user):
        logging.warning("Unauthorized update attempt to expense id: %s by user_id: %s", expense_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this expense"
        )

    db_expense = expense.model_dump(exclude_unset=True)

    for key, value in db_expense.items():
        setattr(expense_exists, key, value)

    db.commit()
    db.refresh(expense_exists)

    logging.info("Expense id: %s updated for user_id: %s", expense_id, current_user.id)
    return SuccessResponse(
        message="Expense updated successfully",
        data=expense_exists
    )

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(
        require([Permission.EXPENSE_DELETE])
    ),
    db: Session = Depends(get_db)
):
    """
    Delete an expense entry
    """

    logging.info("Deleting expense id: %s for user_id: %s", expense_id, current_user.id)
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if db_expense is None:
        logging.warning("Expense id: %s not found for user_id: %s", expense_id, current_user.id)
        raise HTTPException(status_code=404, detail="Expense not found")

    if not check_ownership(db_expense, current_user):
        logging.warning("Unauthorized delete attempt to expense id: %s by user_id: %s", expense_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this expense"
        )
    
    db.delete(db_expense)
    db.commit()

    logging.info("Expense id: %s deleted for user_id: %s", expense_id, current_user.id)
    return None
