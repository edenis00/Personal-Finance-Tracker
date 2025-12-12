"""
Docstring for backend.app.routes.savings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Savings, User
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schema.savings import SavingsCreate, SavingsResponse, SavingsUpdate


router = APIRouter(prefix="/savings", tags=["Savings"])


@router.get("/", response_model=SavingsResponse)
def fetch_savings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieving savings for a user
    """
    savings = db.query(Savings).filter(Savings.user_id == current_user.id).first()
    if not savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    return savings


@router.post("/", response_model=SavingsResponse, status_code=status.HTTP_201_CREATED)
def create(
    saving: SavingsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creating new savings for a user
    """
    savings = db.query(Savings).filter(Savings.user_id == current_user.id).first()
    if savings:
        raise HTTPException(status_code=409, detail="Savings already exists for this user")

    new_savings = Savings(**saving.dict)

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    return new_savings


@router.put("/", response_model=SavingsResponse, status_code=status.HTTP_200_OK)
def update(
    savings: SavingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updating savings for a user
    """
    existing_savings = db.query(Savings).filter(Savings.user_id == current_user.id).first()

    if not existing_savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    update_data = savings.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_savings, key, value)

    db.commit()
    db.refresh(existing_savings)

    return existing_savings


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleting savings of a user
    """
    existing_savings = db.query(Savings).filter(Savings.user_id == current_user.id).first()

    if not existing_savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    db.delete(existing_savings)
    db.commit()

    return None
