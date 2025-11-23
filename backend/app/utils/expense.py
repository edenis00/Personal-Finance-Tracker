"""
Expense utility functions
"""


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
