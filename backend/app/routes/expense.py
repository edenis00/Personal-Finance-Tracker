"""
Expense routes 
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Expense, User
from app.dependencies.auth import get_current_user
from app.utils.expense import calculate_total_expenses, filter_expenses_by_category
from app.schema.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    """
    Create a new expense entry
    """

    db_expense = Expense(**expense.model_dump(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve an expense entry by ID
    """

    expense_exists = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense_exists:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense_exists


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing expense entry
    """

    expense_exists = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if expense_exists is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    db_expense = expense.model_dump(exclude_unset=True)

    for key, value in db_expense.items():
        setattr(expense_exists, key, value)

    db.commit()
    db.refresh(expense_exists)

    return expense_exists

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an expense entry
    """

    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(db_expense)
    db.commit()

    return None


@router.get("/total/")
def get_total_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate total expenses for a user
    """

    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        return {"user_id": current_user.id, "total_expenses": 0.0}

    total = calculate_total_expenses(expenses)

    return {"user_id": current_user.id, "total_expenses": total}


@router.get("/category/{category}", response_model=list[ExpenseResponse])
def get_expenses_by_category(
    category: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve expenses for a user filtered by category
    """

    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this user")
    
    filtered_expenses = filter_expenses_by_category(expenses, category)

    return filtered_expenses
