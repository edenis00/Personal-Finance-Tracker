"""
Docstring for backend.app.utils.savings
"""
from app.models import Savings


def savings_exists(user_id, db):
    """
    Docstring for check_savings
    
    :param user_id: Description
    :param db: Description
    """
    try:
        if user_id:
            user = db.query(Savings).filter(Savings.user_id == user_id).first()
    except Exception as e:
        return f"Error occured due: {e}"

    return user is not None
