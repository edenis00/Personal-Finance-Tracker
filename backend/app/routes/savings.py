"""
Docstring for backend.app.routes.savings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Savings
from app.db.database import get_db
from app.schema.savings import SavingsCreate, SavingsResponse, SavingsUpdate


router = APIRouter(prefix="/savings", tags=["Savings"])


@router.get("/{user_id}", response_model=SavingsResponse, status_code=status.HTTP_200_OK)
def fetch_savings(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieving savings for a user
    """
    savings = db.get(Savings, user_id)
    if not savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    return savings


@router.post("/", response_model=SavingsResponse, status_code=status.HTTP_201_CREATED)
def create(saving: SavingsCreate, db: Session = Depends(get_db)):
    """
    Creating new savings for a user
    """
    if db.get(Savings, saving.user_id):
        raise HTTPException(status_code=409, detail="Savings already exists for this user")

    new_savings = Savings(**saving.dict)

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    return new_savings


@router.put("/{user_id}", response_model=SavingsResponse, status_code=status.HTTP_200_OK)
def update(user_id: int, savings: SavingsUpdate, db: Session = Depends(get_db)):
    """
    Updating savings for a user
    """
    existing_savings = db.get(Savings, user_id)

    if not existing_savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    update_data = savings.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_savings, key, value)

    db.commit()
    db.refresh(existing_savings)

    return existing_savings


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_db)):
    """
    Deleting savings of a user
    """
    existing_savings = db.get(Savings, user_id)

    if not existing_savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    db.delete(existing_savings)
    db.commit()

    return None
