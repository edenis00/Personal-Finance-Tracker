"""
Income routes
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import User
from app.schema.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.schema.base import SuccessResponse
from app.core.permissions import Permission
from app.dependencies.rbac import require_permissions as require
from app.services.income_service import (
    create_income_service,
    fetch_all_income_service,
    fetch_income_service,
    update_income_service,
    delete_income_service,
    IncomeNotFoundError,
    UserNotFoundError,
)


router = APIRouter(
    prefix="/incomes",
    tags=["incomes"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=SuccessResponse[IncomeResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_income(
    income: IncomeCreate,
    current_user: User = Depends(require([Permission.INCOME_WRITE])),
    db: Session = Depends(get_db),
):
    """
    Create a new income entry
    """
    logging.info(
        "Creating income for user_id: %s, amount: %s, source: %s",
        current_user.id,
        income.amount,
        income.source,
    )
    try:
        new_income = create_income_service(income, current_user, db)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error updating income: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info(
        "Income created with id: %s for user_id: %s", new_income.id, current_user.id
    )
    return SuccessResponse(message="Income created successfully", data=new_income)


@router.get("/", response_model=SuccessResponse[list[IncomeResponse]])
def read_incomes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require([Permission.INCOME_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieve all income entries for the current user
    """
    logging.info("Fetching incomes for user_id: %s", current_user.id)
    try:
        incomes = fetch_all_income_service(current_user, db, skip, limit)
    except Exception as e:
        logging.error("Unexpected error updating income: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Found %d incomes for user_id: %s", len(incomes), current_user.id)
    return SuccessResponse(message="Incomes retrieved successfully", data=incomes)


@router.get("/{income_id}", response_model=SuccessResponse[IncomeResponse])
def read_income(
    income_id: int,
    current_user: User = Depends(require([Permission.INCOME_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieve an income entry by ID
    """
    logging.info("Fetching income id: %s for user_id: %s", income_id, current_user.id)
    try:
        income = fetch_income_service(income_id, current_user, db)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except IncomeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Income not found"
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error fetching income: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Income id: %s found for user_id: %s", income_id, current_user.id)
    return SuccessResponse(message="Income retrieved successfully", data=income)


@router.put("/{income_id}", response_model=SuccessResponse[IncomeResponse])
def update_income(
    income_id: int,
    income: IncomeUpdate,
    current_user: User = Depends(require([Permission.INCOME_WRITE])),
    db: Session = Depends(get_db),
):
    """
    Update an existing income entry
    """
    logging.info("Updating income id: %s for user_id: %s", income_id, current_user.id)
    try:
        income = update_income_service(income_id, income, current_user, db)
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income not found"
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error updating income: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Income id: %s updated for user_id: %s", income_id, current_user.id)
    return SuccessResponse(message="Income updated successfully", data=income)


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
    income_id: int,
    current_user: User = Depends(require([Permission.INCOME_DELETE])),
    db: Session = Depends(get_db),
):
    """
    Delete an income entry
    """

    logging.info("Deleting income id: %s for user_id: %s", income_id, current_user.id)
    try:
        income = delete_income_service(income_id, current_user, db)
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IncomeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income not found"
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error deleting income: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Income id: %s deleted for user_id: %s", income_id, current_user.id)
    return None
