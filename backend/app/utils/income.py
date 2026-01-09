"""
Income utilities
"""
import logging
from collections import defaultdict
from app.core.permissions import Role
from sqlalchemy.orm import Session
from app.models import Income, User
from app.schema.income import IncomeCreate, IncomeUpdate

logger = logging.getLogger(__name__)

class IncomeNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def create_income_service(income: IncomeCreate, current_user: User, db: Session) -> Income:
    """
    Creating income and adding balance
    Args:
        income: Income data to create
        current_user: user data to create income
    Return:
        Expense Data
    """
    try:
        user = db.query(User).filter(User.id == current_user.id).with_for_update().first()
        if not user:
            raise UserNotFoundError("User not Found")
        
        new_income = Income(**income.model_dump(), user_id=current_user.id)
        db.add(new_income)
        user.balance += new_income.amount
        db.commit()
        db.refresh(new_income)
        return new_income
    
    except Exception as e:
        db.rollback()
        logging.warning(f"Failed to create income for user {current_user.id} due to: {str(e)}")
        raise e


def fetch_all_income_service(current_user: User, db: Session, skip: int=0, limit: int=100) -> Income:
    """
    Retrieveing all incomes
    Args:
        skip: start count of rows
        limit: end count of rows
        current_user: authorized user data
        db: session of db
    return:
        incomes
    """
    try:
        logging.info("Retrieveing all incomes for user_id: %s", current_user.id)
        incomes = db.query(Income).filter(Income.user_id == current_user.id).offset(skip).limit(limit).all()
        return incomes
    except Exception as e:
        logging.warning(f"Failed to read incomes of user: {current_user.id} due to: {str(e)}")
        raise e


def fetch_income_service(income_id: int, current_user: User, db: Session) -> Income:
    """
    Retrieveing income by id
    Args:
        income_id: Id of income model
        current_user: data of logged in user
        db: session of db
    return:
        incomes
    """
    try:
        
        logging.info("Retrieveing incomes id: %s for user_id: %s", income_id, current_user.id)
        income = db.query(Income).filter(Income.id == income_id).first()
        if not income:
            logging.warning("Income id %s for user_id %s noy found", income_id, current_user.id)
            raise IncomeNotFoundError("Income not found")
        
        if not authorized(income, current_user):
            raise ValueError("Unauthorized to access this income")
        return income
    except Exception as e:
        logging.warning(f"Failed to read incomes of user: {current_user.id} due to: {str(e)}")
        raise e


def update_income_service(
    income_id: int,
    income_update:IncomeUpdate,
    current_user: User,
    db: Session
):
    """
    Updateding income by ID
    Args:
        income_id: Id of selected income
        income: data of income
        current_user: data of logged in user
        db: session of db
    return:
        incomes
    """
    logging.info("Updating income id: %s for user_id: %s", income_id, current_user.id)
    try:
        income = db.query(Income).filter(Income.id == income_id).with_for_update().first()
        
        if income is None:
            logging.warning("Income: %s for user %s not found", income_id, current_user.id)
            raise IncomeNotFoundError(f"Income {income_id} not found")
        
        if not authorized(income, current_user):
            raise ValueError("Unauthorized to edit this income")
        
        user = db.query(User).filter(User.id == current_user.id).with_for_update().first()
        if not user:
            raise UserNotFoundError(f"User {current_user.id} not found")
        old_amount = income.amount
        new_amount = income_update.amount if income_update.amount is not None else old_amount
        difference = old_amount - new_amount
        user.balance -= difference
        
        if income_update.amount is not None:
            income.amount = new_amount
        if income_update.source is not None:
            income.source = income_update.source
        if income_update.date is not None:
            income.date = income_update.date
        
        db.commit()
        db.refresh(income)
        return income
    except Exception as e:
        db.rollback()
        raise e

 
def delete_income_service(
    income_id: int,
    current_user: User,
    db: Session
  ):
    """
    Deleteing an income with ID
    Args:
        income_id: Id of selected income
        current_user: Data of logged in user
        db: Session of db
    return:
        income
    """
    try:
        income = db.query(Income).filter(Income.id == income_id).with_for_update().first()
        
        if not income:
            logging.warning("Income %s not found for user_id %s", income_id, current_user.id)
            raise IncomeNotFoundError("Income not found")
        
        if not authorized(income, current_user):
            raise ValueError("Unauthorized to delete income")
        
        user = db.query(User).filter(User.id == current_user.id).with_for_update().first()
        if not user:
            raise UserNotFoundError(f"User {current_user.id} not found")
        
        db.delete(income)
        user.balance -= income.amount
        db.commit()
        return income
    except Exception as e:
        db.rollback()
        raise e
    
def authorized(income, current_user):
    """
    Check if the income belongs to the given user
    """
    return income.user_id == current_user.id


def calculate_total_income(incomes):
    """
    Calculate the total income from a list of income entries
    """
    return sum(income.amount for income in incomes)


def filter_incomes_by_source(incomes, source):
    """
    Filter income entries by source
    """
    return [income for income in incomes if income.source == source]


def get_recent_incomes(incomes, n=5):
    """
    Get the most recent n income entries
    """
    sorted_incomes = sorted(incomes, key=lambda x: x.date, reverse=True)
    return sorted_incomes[:n]


def group_incomes_by_month(incomes):
    """
    Group income entries by month
    """
    grouped = defaultdict(list)
    for income in incomes:
        month = income.date.strftime("%Y-%m")
        grouped[month].append(income)
    return dict(grouped)


def average_income(incomes):
    """
    Calculate the average income from a list of income entries
    """
    if not incomes:
        return 0
    total = calculate_total_income(incomes)
    return total / len(incomes)


def max_income(incomes):
    """
    Get the maximum income entry
    """
    if not incomes:
        return None
    return max(incomes, key=lambda x: x.amount)


def min_income(incomes):
    """
    Get the minimum income entry
    """
    if not incomes:
        return None
    return min(incomes, key=lambda x: x.amount)
