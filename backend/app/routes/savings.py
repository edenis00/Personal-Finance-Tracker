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
from app.services.savings_service import (
    get_saving_service,
    get_all_savings_service,
    create_saving_service,
    update_saving_service,
    delete_saving_service,
)


router = APIRouter(prefix="/savings", tags=["Savings"])

logger = logging.getLogger(__name__)


@router.get("/{savings_id}", response_model=SuccessResponse[SavingsResponse])
def read_saving(
    savings_id: int,
    current_user: User = Depends(require([Permission.SAVINGS_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieving savings for a user
    """

    try:
        savings = get_saving_service(savings_id, current_user, db)
        if not savings:
            raise HTTPException(status_code=404, detail="Savings not found")
        return SuccessResponse(message="Savings retrieved successfully", data=savings)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/", response_model=SuccessResponse[list[SavingsResponse]])
def read_savings(
    current_user: User = Depends(require([Permission.SAVINGS_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieving all savings for a user
    """
    savings_list = get_all_savings_service(current_user, db)
    return SuccessResponse(message="Savings retrieved successfully", data=savings_list)


@router.post(
    "/",
    response_model=SuccessResponse[SavingsResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(
    saving: SavingsCreate,
    current_user: User = Depends(require([Permission.SAVINGS_READ])),
    db: Session = Depends(get_db),
):
    """
    Creating new savings for a user
    """

    try:
        new_savings = create_saving_service(saving, current_user, db)
        return SuccessResponse(message="Savings created successfully", data=new_savings)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.put(
    "/{savings_id}",
    response_model=SuccessResponse[SavingsResponse],
    status_code=status.HTTP_200_OK,
)
def update(
    savings_id: int,
    savings: SavingsUpdate,
    current_user: User = Depends(require([Permission.SAVINGS_READ])),
    db: Session = Depends(get_db),
):
    """
    Updating savings for a user
    """
    try:
        existing_savings = update_saving_service(savings_id, savings, current_user, db)
        if not existing_savings:
            raise HTTPException(status_code=404, detail="Savings not found")
        return SuccessResponse(
            message="Savings updated successfully", data=existing_savings
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.delete("/{savings_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    savings_id: int,
    current_user: User = Depends(require([Permission.SAVINGS_DELETE])),
    db: Session = Depends(get_db),
):
    """
    Deleting savings of a user
    """
    try:
        existing_savings = delete_saving_service(savings_id, current_user, db)
        if not existing_savings:
            raise HTTPException(status_code=404, detail="Savings not found")
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
