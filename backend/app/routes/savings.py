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


@router.get("/{savings_id}", response_model=SavingsResponse)
def read_saving(
    savings_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieving savings for a user
    """

    savings = db.query(Savings).filter(
        Savings.id == savings_id,
        Savings.user_id == current_user.id
    ).first()

    if not savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    return savings


@router.get("/", response_model=list[SavingsResponse])
def read_savings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieving all savings for a user
    """

    savings_list = db.query(Savings).filter(
        Savings.user_id == current_user.id
    ).all()

    if not savings_list:
        raise HTTPException(status_code=404, detail="No savings found")

    return savings_list


@router.post("/", response_model=SavingsResponse, status_code=status.HTTP_201_CREATED)
def create(
    saving: SavingsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creating new savings for a user
    """

    new_savings = Savings(**saving.model_dump(), user_id=current_user.id)

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    return new_savings


@router.put("/{savings_id}", response_model=SavingsResponse, status_code=status.HTTP_200_OK)
def update(
    savings_id: int,
    savings: SavingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updating savings for a user
    """
    existing_savings = db.query(Savings).filter(
        Savings.user_id == current_user.id,
        Savings.id == savings_id
    ).first()

    if not existing_savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    update_data = savings.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_savings, key, value)

    db.commit()
    db.refresh(existing_savings)

    return existing_savings


@router.delete("/{savings_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    savings_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleting savings of a user
    """
    existing_savings = db.query(Savings).filter(
        Savings.id == savings_id,
        Savings.user_id == current_user.id
    ).first()

    if not existing_savings:
        raise HTTPException(status_code=404, detail="Savings not found")

    db.delete(existing_savings)
    db.commit()

    return None
