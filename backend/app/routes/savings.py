"""
Docstring for backend.app.routes.savings
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Savings, User
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schema.savings import SavingsCreate, SavingsResponse, SavingsUpdate


router = APIRouter(prefix="/savings", tags=["Savings"])

logger = logging.getLogger(__name__)

@router.get("/{savings_id}", response_model=SavingsResponse)
def read_saving(
    savings_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieving savings for a user
    """

    logging.info("Fetching savings id: %s for user_id: %s", savings_id, current_user.id)
    savings = db.query(Savings).filter(
        Savings.id == savings_id,
        Savings.user_id == current_user.id
    ).first()

    if not savings:
        logging.warning("Savings id: %s not found for user_id: %s", savings_id, current_user.id)
        raise HTTPException(status_code=404, detail="Savings not found")

    logging.info("Savings id: %s retrieved for user_id: %s", savings_id, current_user.id)
    return savings


@router.get("/", response_model=list[SavingsResponse])
def read_savings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieving all savings for a user
    """
    logging.info("Fetching all savings for user_id: %s", current_user.id)

    savings_list = db.query(Savings).filter(
        Savings.user_id == current_user.id
    ).all()

    logging.info("Found %d savings for user_id: %s", len(savings_list), current_user.id)
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

    logging.info("Creating savings for user_id: %s, amount: %s, goal: %s", current_user.id, saving.amount, saving.goal)
    new_savings = Savings(**saving.model_dump(), user_id=current_user.id)

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    logging.info("Savings created with id: %s for user_id: %s", new_savings.id, current_user.id)
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
    logging.info("Updating savings id: %s for user_id: %s", savings_id, current_user.id)
    existing_savings = db.query(Savings).filter(
        Savings.user_id == current_user.id,
        Savings.id == savings_id
    ).first()

    if not existing_savings:
        logging.warning("Savings id: %s not found for user_id: %s", savings_id, current_user.id)
        raise HTTPException(status_code=404, detail="Savings not found")

    update_data = savings.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_savings, key, value)

    db.commit()
    db.refresh(existing_savings)

    logging.info("Savings id: %s updated for user_id: %s", savings_id, current_user.id)
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
    logging.info("Deleting savings id: %s for user_id: %s", savings_id, current_user.id)
    existing_savings = db.query(Savings).filter(
        Savings.id == savings_id,
        Savings.user_id == current_user.id
    ).first()

    if not existing_savings:
        logging.warning("Savings id: %s not found for user_id: %s", savings_id, current_user.id)
        raise HTTPException(status_code=404, detail="Savings not found")

    db.delete(existing_savings)
    db.commit()

    logging.info("Savings id: %s deleted for user_id: %s", savings_id, current_user.id)
    return None
