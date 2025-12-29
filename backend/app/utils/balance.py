from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models import User, Expense, Income, Savings


def get_user_balance(
    current_user: User,
    db: Session
):
    """
    Get balance of a user
    """
    total_income =  db.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id
    ).scalar() or 0

    total_expense = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id
    ).scalar() or 0

    total_savings = db.query(func.sum(Savings.amount)).filter(
        Savings.user_id == current_user.id
    ).scalar() or 0

    available_balance = total_income - total_expense - total_savings
    net_balance = total_income - total_expense
    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "total_savings": float(total_savings),
        "balance": float(available_balance),
        "net_balance": float(net_balance)
    }


def has_sufficient_balance(
    current_user: User,
    db: Session,
    amount: float,
    allow_overdraft: bool = False
) -> bool:
    """
    Check if user has sufficient balance for a given amount
    """
    if allow_overdraft:
        return True
    balance_data = get_user_balance(current_user, db)
    return balance_data["balance"] >= amount
