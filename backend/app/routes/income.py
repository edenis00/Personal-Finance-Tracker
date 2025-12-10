"""
Income routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.income import Income
from app.schema.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.utils.income import (
    calculate_total_income,
    get_recent_incomes,
    check_income_exists,
    check_income_validity
)

router = APIRouter(
    prefix="/incomes",
    tags=["incomes"],
)


@router.post("/", response_model=IncomeResponse)
def create_income(income: IncomeCreate, db: Session = Depends(get_db)):
    """
    Create a new income entry
    """
    new_income = Income(**income.dict())

    try:
        if not check_income_validity(new_income):
            raise HTTPException(status_code=400, detail="Invalid income data")
        db.add(new_income)
        db.commit()
        db.refresh(new_income)
    except Exception as e:
        db.rollback()
        raise e

    return new_income


@router.get("/{income_id}", response_model=IncomeResponse)
def read_income(income_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an income entry by ID
    """
    db_income = check_income_exists(income_id, Income, db)

    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")

    return db_income


@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(income_id: int, income: IncomeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing income entry
    """
    db_income = check_income_exists(income_id, Income, db)

    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")

    for key, value in income.dict().items():
        setattr(db_income, key, value)

    try:
        if not check_income_validity(db_income):
            raise HTTPException(status_code=400, detail="Invalid income data")
        db.commit()
        db.refresh(db_income)
    except Exception as e:
        db.rollback()
        raise e

    return db_income


@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    """
    Delete an income entry
    """

    db_income = check_income_exists(income_id, Income, db)

    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")

    try:
        db.delete(db_income)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return {"detail": "Income deleted successfully"}


@router.get("/", response_model=List[IncomeResponse])
def read_incomes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve income entries
    """

    incomes = db.query(Income).offset(skip).limit(limit).all()

    return incomes


@router.get("/total/", response_model=float)
def get_total_income(db: Session = Depends(get_db)):
    """
    Get the total income from all entries
    """

    incomes = db.query(Income).all()
    total = calculate_total_income(incomes)

    return total


@router.get("/recent/", response_model=List[IncomeResponse])
def get_recent_income_entries(n: int = 5, db: Session = Depends(get_db)):
    """
    Get the most recent n income entries
    """

    incomes = db.query(Income).all()
    recent_incomes = get_recent_incomes(incomes, n)

    return recent_incomes
