"""
Income routes
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Income, User
from app.schema.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.dependencies.auth import get_current_user
from app.utils.income import (
    check_income_validity
)


router = APIRouter(
    prefix="/incomes",
    tags=["incomes"],
)

logger = logging.getLogger(__name__)

@router.post("/", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(
    income: IncomeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new income entry
    """
    logging.info("Creating income for user_id: %s, amount: %s, source: %s", current_user.id, income.amount, income.source)
    new_income = Income(**income.model_dump(), user_id=current_user.id)

    if not check_income_validity(new_income):
        logging.warning("Invalid income data for user_id: %s", current_user.id)
        raise HTTPException(status_code=400, detail="Invalid income data")

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    logging.info("Income created with id: %s for user_id: %s", new_income.id, current_user.id)
    return new_income


@router.get("/{income_id}", response_model=IncomeResponse)
def read_income(
    income_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve an income entry by ID
    """
    logging.info("Fetching income id: %s for user_id: %s", income_id, current_user.id)
    check_income_exists = db.query(Income).filter(
        Income.user_id == current_user.id,
        Income.id == income_id
    ).first()

    if not check_income_exists:
        logging.warning("Income id: %s not found for user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=404, detail="Income not found")

    logging.info("Income id: %s found for user_id: %s", income_id, current_user.id)
    return check_income_exists


@router.get("/", response_model=list[IncomeResponse])
def read_incomes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all income entries for the current user
    """
    logging.info("Fetching incomes for user_id: %s", current_user.id)
    incomes = db.query(Income).filter(Income.user_id == current_user.id).all()

    logging.info("Found %d incomes for user_id: %s", len(incomes), current_user.id)
    return incomes


@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(
    income_id: int,
    income: IncomeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing income entry
    """
    logging.info("Updating income id: %s for user_id: %s", income_id, current_user.id)
    check_income_exists = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == current_user.id
    ).first()

    if check_income_exists is None:
        logging.warning("Income id: %s not found for user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=404, detail="Income not found")

    if not check_income_validity(check_income_exists):
        logging.warning("Invalid income data for income id: %s, user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=400, detail="Invalid income data")

    income_data = income.model_dump(exclude_unset=True)
    for key, value in income_data.items():
        setattr(check_income_exists, key, value)

    db.commit()
    db.refresh(check_income_exists)

    logging.info("Income id: %s updated for user_id: %s", income_id, current_user.id)
    return check_income_exists


@router.delete("/{income_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
    income_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an income entry
    """

    logging.info("Deleting income id: %s for user_id: %s", income_id, current_user.id)
    check_income_exists = db.query(Income).filter(
        Income.user_id == current_user.id,
        Income.id == income_id
    ).first()

    if check_income_exists is None:
        logging.warning("Income id: %s not found for user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=404, detail="Income not found")

    db.delete(check_income_exists)
    db.commit()

    logging.info("Income id: %s deleted for user_id: %s", income_id, current_user.id)
    return None
