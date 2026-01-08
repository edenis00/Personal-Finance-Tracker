"""
Expense utility functions
"""

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app.models import User, Expense
from app.schema.expense import ExpenseCreate, ExpenseUpdate
from app.core.permissions import Role
import logging

logger = logging.getLogger(__name__)


class InsufficientBalanceError(Exception):
    pass


class ExpenseNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def create_expense_service(
    expense: ExpenseCreate, current_user_id: int, db: Session
) -> Expense:
    """
    Creating a expense service and deduct from user balance
    Args:
        expense: Expense data to create
        current_user_id: ID of the user creating the expense
    """
    try:
        user = (
            db.query(User).filter(User.id == current_user_id).with_for_update().first()
        )

        if not user:
            raise UserNotFoundError("User not found")

        if user.balance < expense.amount:
            raise InsufficientBalanceError("Insufficent Amount")

        expense = Expense(**expense.model_dump(), user_id=current_user_id)
        user.balance -= expense.amount
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense
    except Exception as e:
        db.rollback()
        logging.error("Failed to create expense %s: %s", expense.id, str(e))
        raise e


def read_all_expense_service(
    current_user: User, db: Session, skip: int = 0, limit: int = 100
):
    """
    Read expense service
    """
    if current_user.role == Role.ADMIN.value:
        logging.info("Admin user_id: %s fetching all expenses", current_user.id)
        expenses = db.query(Expense).offset(skip).limit(limit).all()

    logger.info("Fetching expense for user_id: %s", current_user.id)
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return expenses


def read_expense_service(
    expense_id: int,
    db: Session,
):
    """
    Read a particular expense by id
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise ExpenseNotFoundError("Expense not Found")

    return expense


def update_expense_service(
    expense_id: int, expense_update: ExpenseUpdate, current_user: User, db: Session
) -> Expense:
    """
    Update an existing expense
    """
    try:
        expense = (
            db.query(Expense).filter(Expense.id == expense_id).with_for_update().first()
        )
        if not expense:
            raise ExpenseNotFoundError(f"Expense {expense.id} not found")

        if not is_authorized(expense, current_user):
            raise ValueError("Unauthorized to update this expense")

        user = (
            db.query(User).filter(User.id == current_user.id).with_for_update().first()
        )
        if not user:
            raise UserNotFoundError("User not found")

        old_amount = expense.amount
        new_amount = (
            expense_update.amount if expense_update.amount is not None else old_amount
        )
        difference = new_amount - old_amount

        if difference > 0:
            if user.balance < difference:
                raise InsufficientBalanceError(
                    f"Insufficient balance. For {expense.amount} this balance: {user.balance}"
                )

        if expense_update.amount is not None:
            expense.amount = new_amount
        if expense_update.category is not None:
            expense.category = expense_update.category
        if expense_update.date is not None:
            expense.date = expense_update.date

        user.balance -= difference

        db.commit()
        db.refresh(expense)
        return expense
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update expense {expense_id} due to: {str(e)}")
        raise e


def is_authorized(expense, current_user) -> bool:
    """
    Check if the expense belongs to the given user or user is admin
    """
    return expense.user_id == current_user.id or current_user.role == Role.ADMIN.value


def delete_expense_service(expense_id: int, current_user: User, db: Session):
    """
    Docstring for delete_expense_service
    """
    try:
        user = (
            db.query(User).filter(User.id == current_user.id).with_for_update().first()
        )
        if not user:
            raise UserNotFoundError("User not found")

        expense = (
            db.query(Expense).filter(Expense.id == expense_id).with_for_update().first()
        )
        if not expense:
            raise ExpenseNotFoundError("Expense %s not found", expense_id)

        if not is_authorized(expense, current_user):
            logging.warning(
                f"Unauthorized delete attempt to expense id: {expense_id} by user_id: {current_user.id}",
            )
            raise ValueError("Unauthorized to delete this expense")

        db.delete(expense)

        # refund balance
        user.balance += expense.amount
        db.commit()
        return expense
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete expense {expense_id} due to: {str(e)}")
        raise e


def calculate_total_expenses(expenses):
    """
    Calculate the total amount of expenses from a list of expense entries
    """
    return sum(expense.amount for expense in expenses)


def filter_expenses_by_category(expenses, category):
    """
    Filter expenses by a specific category
    """
    return [expense for expense in expenses if expense.category == category]
