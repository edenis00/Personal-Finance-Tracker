"""
Income utilities
"""

from collections import defaultdict
from app.models import Income, User
from app.schema.income import IncomeCreate, IncomeUpdate


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
