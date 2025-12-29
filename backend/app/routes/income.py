"""
Income routes
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Income, User
from app.schema.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.utils.income import check_income_validity, check_ownership
from app.schema.base import SuccessResponse
from app.core.permissions import Permission, Role
from app.dependencies.rbac import require_permissions as require


router = APIRouter(
    prefix="/incomes",
    tags=["incomes"],
)

logger = logging.getLogger(__name__)

@router.post("/", response_model=SuccessResponse[IncomeResponse], status_code=status.HTTP_201_CREATED)
def create_income(
    income: IncomeCreate,
    current_user: User = Depends(
        require([Permission.INCOME_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """
    Create a new income entry
    """
    logging.info("Creating income for user_id: %s, amount: %s, source: %s", current_user.id, income.amount, income.source)
    new_income = Income(**income.model_dump(), user_id=current_user.id)

    if not check_income_validity(new_income):
        logging.warning("Invalid income data for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid income data"
        )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    logging.info("Income created with id: %s for user_id: %s", new_income.id, current_user.id)
    return SuccessResponse(
        message="Income created successfully",
        data=new_income
    )


@router.get("/{income_id}", response_model=SuccessResponse[IncomeResponse])
def read_income(
    income_id: int,
    current_user: User = Depends(
        require([Permission.INCOME_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve an income entry by ID
    """
    logging.info("Fetching income id: %s for user_id: %s", income_id, current_user.id)
    check_income_exists = db.query(Income).filter(Income.id == income_id).first()

    if not check_income_exists:
        logging.warning("Income id: %s not found for user_id: %s", income_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income not found"
        )
    
    if not check_ownership(check_income_exists, current_user):
        logging.warning("Unauthorized access attempt to income id: %s by user_id: %s", income_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this income"
        ) 

    logging.info("Income id: %s found for user_id: %s", income_id, current_user.id)
    return SuccessResponse(
        message="Income retrieved successfully",
        data=check_income_exists
    )


@router.get("/", response_model=SuccessResponse[list[IncomeResponse]])
def read_incomes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(
        require([Permission.INCOME_READ])
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve all income entries for the current user
    """
    logging.info("Fetching incomes for user_id: %s", current_user.id)

    if current_user.role == Role.ADMIN.value:
        # Admin can see all incomes
        logging.info("Admin user_id: %s fetching all incomes", current_user.id)
        incomes = db.query(Income).offset(skip).limit(limit).all()
    else:
        # Regular users can see only their own incomes
        logging.info("Fetching income for user_id: %s", current_user.id)
        incomes = db.query(Income).filter(Income.user_id == current_user.id).offset(skip).limit(limit).all()

    logging.info("Found %d incomes for user_id: %s", len(incomes), current_user.id)
    return SuccessResponse(
        message="Incomes retrieved successfully",
        data=incomes
    )


@router.put("/{income_id}", response_model=SuccessResponse[IncomeResponse])
def update_income(
    income_id: int,
    income: IncomeUpdate,
    current_user: User = Depends(
        require([Permission.INCOME_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """
    Update an existing income entry
    """
    logging.info("Updating income id: %s for user_id: %s", income_id, current_user.id)
    check_income_exists = db.query(Income).filter(Income.id == income_id).first()

    if check_income_exists is None:
        logging.warning("Income id: %s not found for user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=404, detail="Income not found")
    
    if not check_ownership(check_income_exists, current_user):
        logging.warning("Unauthorized update attempt to income id: %s by user_id: %s", income_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this income"
        )

    if not check_income_validity(check_income_exists):
        logging.warning("Invalid income data for income id: %s, user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=400, detail="Invalid income data")

    income_data = income.model_dump(exclude_unset=True)
    for key, value in income_data.items():
        setattr(check_income_exists, key, value)

    db.commit()
    db.refresh(check_income_exists)

    logging.info("Income id: %s updated for user_id: %s", income_id, current_user.id)
    return SuccessResponse(
        meessage="Income updated successfully",
        data=check_income_exists
    )


@router.delete("/{income_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
    income_id: int,
    current_user: User = Depends(
        require([Permission.INCOME_DELETE])
    ),
    db: Session = Depends(get_db)
):
    """
    Delete an income entry
    """

    logging.info("Deleting income id: %s for user_id: %s", income_id, current_user.id)
    check_income_exists = db.query(Income).filter(Income.id == income_id).first()

    if check_income_exists is None:
        logging.warning("Income id: %s not found for user_id: %s", income_id, current_user.id)
        raise HTTPException(status_code=404, detail="Income not found")

    if not check_ownership(check_income_exists, current_user):
        logging.warning("Unauthorized delete attempt to income id: %s by user_id: %s", income_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this income"
        )

    db.delete(check_income_exists)
    db.commit()

    logging.info("Income id: %s deleted for user_id: %s", income_id, current_user.id)
    return None
