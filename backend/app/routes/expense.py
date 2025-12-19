"""
Expense routes 
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Expense, User
from app.dependencies.auth import get_current_active_user
from app.utils.expense import calculate_total_expenses, filter_expenses_by_category
from app.schema.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.schema.base import ErrorResponse, SuccessResponse


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

logger = logging.getLogger(__name__)


@router.post("/", response_model=SuccessResponse[ExpenseResponse], status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_active_user),
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


@router.get("/", response_model=list[ExpenseResponse])
def read_expenses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all expense entries for the current user
    """
    logging.info("Fetching expenses for user_id: %s", current_user.id)
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    logging.info("Found %d expenses for user_id: %s", len(expenses), current_user.id)   
    return expenses


@router.get("/total")
def get_total_expenses(
    current_user: User = Depends(get_current_active_user),
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


@router.get("/category/{category}", response_model=list[ExpenseResponse])
def get_expenses_by_category(
    category: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve expenses for a user filtered by category
    """
    logging.info("Fetching expenses for user_id: %s in category: %s", current_user.id, category)
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        logging.warning("No expenses found for user_id: %s", current_user.id)
        raise HTTPException(status_code=404, detail="Expenses not found")

    filtered_expenses = filter_expenses_by_category(expenses, category)
    logging.info("Found %d expenses for user_id: %s in category: %s", len(filtered_expenses), current_user.id, category)
    return filtered_expenses


@router.get("/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
def read_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve an expense entry by ID
    """
    logging.info("Fetching expense id: %s for user_id: %s", expense_id, current_user.id)
    expense_exists = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense_exists:
        logging.warning("Expense id: %s not found for user_id: %s", expense_id, current_user.id)
        raise HTTPException(status_code=404, detail="Expense not found")

    logging.info("Expense id: %s found for user_id: %s", expense_id, current_user.id)
    return SuccessResponse(
        message="Expense retrieved successfully",
        data=expense_exists
    )


@router.put("/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing expense entry
    """
    logging.info("Updating expense id: %s for user_id: %s", expense_id, current_user.id)
    expense_exists = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if expense_exists is None:
        logging.warning("Expense id: %s not found for user_id: %s", expense_id, current_user.id)
        raise HTTPException(status_code=404, detail="Expense not found")

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
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete an expense entry
    """

    logging.info("Deleting expense id: %s for user_id: %s", expense_id, current_user.id)
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if db_expense is None:
        logging.warning("Expense id: %s not found for user_id: %s", expense_id, current_user.id)
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(db_expense)
    db.commit()

    logging.info("Expense id: %s deleted for user_id: %s", expense_id, current_user.id)
    return None
