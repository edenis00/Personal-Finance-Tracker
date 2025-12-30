"""
Docstring for backend.app.routes.savings
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Savings, User
from app.db.database import get_db
from app.schema.savings import SavingsCreate, SavingsResponse, SavingsUpdate
from app.schema.base import SuccessResponse
from app.core.permissions import Permission, Role
from app.dependencies.rbac import require_permissions as require
from app.utils.savings import is_authorized


router = APIRouter(prefix="/savings", tags=["Savings"])

logger = logging.getLogger(__name__)

@router.get("/{savings_id}", response_model=SuccessResponse[SavingsResponse])
def read_saving(
    savings_id: int,
    current_user: User = Depends(
        require([Permission.SAVINGS_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieving savings for a user
    """

    logging.info("Fetching savings id: %s for user_id: %s", savings_id, current_user.id)
    savings = db.query(Savings).filter(Savings.id == savings_id).first()

    if not savings:
        logging.warning("Savings id: %s not found for user_id: %s", savings_id, current_user.id)
        raise HTTPException(status_code=404, detail="Savings not found")
    
    if is_authorized(savings, current_user):
        logging.warning("Unauthorized access attempt to savings id: %s by user_id: %s", savings_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this savings"
        )

    logging.info("Savings id: %s retrieved for user_id: %s", savings_id, current_user.id)

    return SuccessResponse(
        message="Savings retrieved successfully",
        data=savings
    )


@router.get("/", response_model=SuccessResponse[list[SavingsResponse]])
def read_savings(
    current_user: User = Depends(
        require([Permission.SAVINGS_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieving all savings for a user
    """
    logging.info("Fetching all savings for user_id: %s", current_user.id)

    if current_user.role == Role.ADMIN.value:
        logging.info("Admin user_id: %s retrieving all savings entries", current_user.id)
        savings_list = db.query(Savings).all()
    else:
        logging.info("user_id: %s retrieving own savings entries", current_user.id)
        savings_list = db.query(Savings).filter(Savings.user_id == current_user.id).all()

    logging.info("Found %d savings for user_id: %s", len(savings_list), current_user.id)
    return SuccessResponse(
        message="Savings retrieved successfully",
        data=savings_list
    )


@router.post("/", response_model=SuccessResponse[SavingsResponse], status_code=status.HTTP_201_CREATED)
def create(
    saving: SavingsCreate,
    current_user: User = Depends(
        require([Permission.SAVINGS_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Creating new savings for a user
    """

    logging.info("Creating savings for user_id: %s, amount: %s, goal: %s", current_user.id, saving.amount)


    new_savings = Savings(**saving.model_dump(), user_id=current_user.id)

    if is_authorized(new_savings, current_user):
        logging.warning("Unauthorized create attempt by user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create this savings"
        )

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    logging.info("Savings created with id: %s for user_id: %s", new_savings.id, current_user.id)
    return SuccessResponse(
        message="Savings created successfully",
        data=new_savings
    )


@router.put("/{savings_id}", response_model=SuccessResponse[SavingsResponse], status_code=status.HTTP_200_OK)
def update(
    savings_id: int,
    savings: SavingsUpdate,
    current_user: User = Depends(
        require([Permission.SAVINGS_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Updating savings for a user
    """
    logging.info("Updating savings id: %s for user_id: %s", savings_id, current_user.id)
    existing_savings = db.query(Savings).filter(Savings.id == savings_id).first()

    if not existing_savings:
        logging.warning("Savings id: %s not found for user_id: %s", savings_id, current_user.id)
        raise HTTPException(status_code=404, detail="Savings not found")
    
    if is_authorized(existing_savings, current_user):
        logging.warning("Unauthorized update attempt to savings id: %s by user_id: %s", savings_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this savings"
        )

    update_data = savings.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_savings, key, value)

    db.commit()
    db.refresh(existing_savings)

    logging.info("Savings id: %s updated for user_id: %s", savings_id, current_user.id)
    return SuccessResponse(
        message="Savings updated successfully",
        data=existing_savings
    )


@router.delete("/{savings_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    savings_id: int,
    current_user: User = Depends(
        require([Permission.SAVINGS_DELETE])
    ),
    db: Session = Depends(get_db)
):
    """
    Deleting savings of a user
    """
    logging.info("Deleting savings id: %s for user_id: %s", savings_id, current_user.id)
    existing_savings = db.query(Savings).filter(Savings.id == savings_id).first()

    if not existing_savings:
        logging.warning("Savings id: %s not found for user_id: %s", savings_id, current_user.id)
        raise HTTPException(status_code=404, detail="Savings not found")

    if is_authorized(existing_savings, current_user):
        logging.warning("Unauthorized delete attempt to savings id: %s by user_id: %s", savings_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this savings"
        )

    db.delete(existing_savings)
    db.commit()

    logging.info("Savings id: %s deleted for user_id: %s", savings_id, current_user.id)
    return None
