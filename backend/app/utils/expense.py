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


class InsufficentBalanceError(Exception):
    pass


class ExpenseNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def create_expense_service(
    expense: ExpenseCreate, current_user_id: int, db: Session
) -> Expense:
    """
    Creating a expense service
    """
    try:
        user = (
            db.query(User).filter(User.id == current_user_id).with_for_update().first()
        )
        if user.balance < expense.amount:
            raise InsufficentBalanceError("Insufficent Amount")

        expense = Expense(**expense.model_dump(), user_id=current_user_id)
        user.balance -= expense.amount
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense
    except NoResultFound:
        raise UserNotFoundError("User not found")


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
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User,
    db: Session
) -> Expense:
    """
    Update an existing expense
    """
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).with_for_update().first()
        if not expense:
            raise ExpenseNotFoundError("Expense not found")

        if not is_authorized(expense, current_user):
            raise ValueError("Unauthorized to update this expense")

        user = (db.query(User).filter(User.id == current_user.id).with_for_update().first())
        if not user:
            raise UserNotFoundError("User not found")

        old_amount = expense.amount
        new_amount = expense_update.amount if expense_update.amount is not None else old_amount
        diff = new_amount - old_amount

        if diff > 0 and user.balance < diff:
            raise InsufficentBalanceError("Insufficient balance")

        expense.amount = new_amount
        if expense_update.category is not None:
            expense.category = expense_update.category
        expense.date = expense_update.date
        
        user.balance -= diff

        db.commit()
        db.refresh(expense)
        return expense
    except Exception as e:
        db.rollback()
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


def is_authorized(expense, current_user) -> bool:
    """
    Check if the expense belongs to the given user or user is admin
    """
    return expense.user_id == current_user.id or current_user.role == Role.ADMIN.value
