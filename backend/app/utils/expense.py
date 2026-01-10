"""
Expense utility functions
"""

from sqlalchemy.orm import Session
from app.models import User, Expense
from app.schema.expense import ExpenseCreate, ExpenseUpdate
import logging


def is_authorized(expense, current_user) -> bool:
    """
    Check if the expense belongs to the given user
    """
    return expense.user_id == current_user.id


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
