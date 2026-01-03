"""
Expense routes
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Expense, User
from app.schema.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.schema.base import SuccessResponse
from app.core.permissions import Permission
from app.dependencies.rbac import require_permissions as require
from app.utils.expense import (
    calculate_total_expenses,
    filter_expenses_by_category,
    create_expense_service,
    read_all_expense_service,
    read_expense_service,
    update_expense_service,
    delete_expense_service,
    InsufficientBalanceError,
    UserNotFoundError,
    ExpenseNotFoundError,
)


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=SuccessResponse[ExpenseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(require([Permission.EXPENSE_WRITE])),
    db: Session = Depends(get_db),
):
    """
    Create a new expense entry
    """
    logging.info(
        "Creating expense for user_id: %s, amount: %s, category: %s",
        current_user.id,
        expense.amount,
        expense.category,
    )

    try:
        new_expense = create_expense_service(expense, current_user.id, db)
    except InsufficientBalanceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error updating expense: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logger.info(
        "Expense created with id: %s for user_id: %s", new_expense.id, current_user.id
    )
    return SuccessResponse(message="Expense created successfully", data=new_expense)


@router.get("/", response_model=SuccessResponse[list[ExpenseResponse]])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require([Permission.EXPENSE_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieve all expense entries for the current user
    """
    expenses = read_all_expense_service(current_user, db, skip, limit)

    logging.info("Found %d expenses for user_id: %s", len(expenses), current_user.id)
    return SuccessResponse(message="Expenses retrieved successfully", data=expenses)


@router.get("/total")
def get_total_expenses(
    current_user: User = Depends(require([Permission.EXPENSE_READ])),
    db: Session = Depends(get_db),
):
    """
    Calculate total expenses for a user
    """
    logging.info("Calculating total expenses for user_id: %s", current_user.id)
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        logging.warning("No expenses found for user_id: %s", current_user.id)
        return {"user_id": current_user.id, "total_expenses": 0.0}

    total = calculate_total_expenses(expenses)

    logging.info("Total expenses for user_id: %s is %f", current_user.id, total)
    return {"user_id": current_user.id, "total_expenses": total}


@router.get(
    "/category/{category}", response_model=SuccessResponse[list[ExpenseResponse]]
)
def get_expenses_by_category(
    category: str,
    current_user: User = Depends(require([Permission.EXPENSE_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieve expenses for a user filtered by category
    """
    logging.info(
        "Fetching expenses for user_id: %s in category: %s", current_user.id, category
    )
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    if not expenses:
        logging.warning("No expenses found for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expenses not found"
        )

    filtered_expenses = filter_expenses_by_category(expenses, category)
    logging.info(
        "Found %d expenses for user_id: %s in category: %s",
        len(filtered_expenses),
        current_user.id,
        category,
    )
    return SuccessResponse(
        message="Expenses retrieved successfully", data=filtered_expenses
    )


@router.get("/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
def read_expense(
    expense_id: int,
    current_user: User = Depends(require([Permission.EXPENSE_READ])),
    db: Session = Depends(get_db),
):
    """
    Retrieve an expense entry by ID
    """
    logging.info("Fetching expense id: %s for user_id: %s", expense_id, current_user.id)
    try:
        expense = read_expense_service(expense_id, db)
    except ExpenseNotFoundError as e:
        logging.warning(
            "Expense id: %s not found for user_id: %s", expense_id, current_user.id
        )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error updating expense: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Expense id: %s found for user_id: %s", expense_id, current_user.id)
    return SuccessResponse(message="Expense retrieved successfully", data=expense)


@router.put("/{expense_id}", response_model=SuccessResponse[ExpenseResponse])
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(require([Permission.EXPENSE_WRITE])),
    db: Session = Depends(get_db),
):
    """
    Update an existing expense entry
    """
    logging.info("Updating expense id: %s for user_id: %s", expense_id, current_user.id)

    try:
        updated_expense = update_expense_service(
            expense_id, expense_update, current_user, db
        )
    except InsufficientBalanceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except ExpenseNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        logging.error("Unexpected error updating expense: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Expense id: %s updated for user_id: %s", expense_id, current_user.id)
    return SuccessResponse(message="Expense updated successfully", data=updated_expense)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(require([Permission.EXPENSE_DELETE])),
    db: Session = Depends(get_db),
):
    """
    Delete an expense entry
    """

    logging.info("Deleting expense id: %s for user_id: %s", expense_id, current_user.id)
    try:
        expense = delete_expense_service(expense_id, current_user, db)
    except InsufficientBalanceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except ExpenseNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        logging.error("Unexpected error updating expense: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    logging.info("Expense id: %s deleted for user_id: %s", expense_id, current_user.id)
    return None
