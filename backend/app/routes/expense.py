"""
Expense routes 
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.expense import Expense
from app.utils.expense import calculate_total_expenses, filter_expenses_by_category
from app.schema.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)


@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create a new expense entry
    """

    try:
        db_expense = Expense(**expense.dict())
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
    except Exception as e:
        db.rollback()
        raise e

    return db_expense


@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an expense entry by ID
    """

    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return db_expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    """
    Update an existing expense entry
    """

    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in expense.dict().items():
        setattr(db_expense, key, value)

    try:
        db.commit()
        db.refresh(db_expense)
    except Exception as e:
        db.rollback()
        raise e

    return db_expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """
    Delete an expense entry
    """

    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    try:
        db.delete(db_expense)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return {"detail": "Expense deleted successfully"}


@router.get("/total/{user_id}")
def get_total_expenses(user_id: int, db: Session = Depends(get_db)):
    """
    Calculate total expenses for a user
    """

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    total = calculate_total_expenses(expenses)

    return {"user_id": user_id, "total_expenses": total}


@router.get("/category/{user_id}/{category}", response_model=list[ExpenseResponse])
def get_expenses_by_category(user_id: int, category: str, db: Session = Depends(get_db)):
    """
    Retrieve expenses for a user filtered by category
    """

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    filtered_expenses = filter_expenses_by_category(expenses, category)

    return filtered_expenses
