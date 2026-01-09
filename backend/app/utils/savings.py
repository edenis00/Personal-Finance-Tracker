"""
Docstring for backend.app.utils.savings
"""



def is_authorized(savings, current_user) -> bool:
    """
    Check if the savings entry belongs to the user

    :param savings: Savings entry
    :param current_user: Current user object
    :return: True if the savings belongs to the user, False otherwise
    """
    return savings.user_id == current_user.id