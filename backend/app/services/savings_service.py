"""
Savings Service
"""

import logging
from sqlalchemy.orm import Session
from app.models import Savings, User
from app.schema.savings import SavingsCreate, SavingsUpdate
from app.core.permissions import Role

logger = logging.getLogger(__name__)


def is_authorized(savings, current_user) -> bool:
    """
    Check if the savings entry belongs to the user
    """
    return savings.user_id == current_user.id


def get_saving_service(savings_id: int, current_user: User, db: Session):
    """
    Retrieving savings for a user
    """
    logger.info("Fetching savings id: %s for user_id: %s", savings_id, current_user.id)
    savings = db.query(Savings).filter(Savings.id == savings_id).first()

    if not savings:
        logger.warning(
            "Savings id: %s not found for user_id: %s", savings_id, current_user.id
        )
        return None

    if not is_authorized(savings, current_user):
        logger.warning(
            "Unauthorized access attempt to savings id: %s by user_id: %s",
            savings_id,
            current_user.id,
        )
        raise ValueError("Unauthorized access")

    logger.info("Savings id: %s retrieved for user_id: %s", savings_id, current_user.id)
    return savings


def get_all_savings_service(current_user: User, db: Session):
    """
    Retrieving all savings for a user
    """
    logger.info("Fetching all savings for user_id: %s", current_user.id)

    try:
        logger.info("user_id: %s retrieving own savings entries", current_user.id)
        savings_list = (
            db.query(Savings).filter(Savings.user_id == current_user.id).all()
        )
    except Exception as e:
        logger.warning(
            "Failed to retrieve savings for user_id: %s due to: %s", current_user.id, e
        )
        raise e

    return savings_list


def create_saving_service(saving: SavingsCreate, current_user: User, db: Session):
    """
    Creating new savings for a user
    """
    logger.info(
        "Creating savings for user_id: %s, amount: %s, goal: %s",
        current_user.id,
        saving.amount,
        saving.goal,
    )

    new_savings = Savings(**saving.model_dump(), user_id=current_user.id)

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    logger.info(
        "Savings created with id: %s for user_id: %s", new_savings.id, current_user.id
    )
    return new_savings


def update_saving_service(
    savings_id: int, saving_update: SavingsUpdate, current_user: User, db: Session
):
    """
    Updating savings for a user
    """
    logger.info("Updating savings id: %s for user_id: %s", savings_id, current_user.id)
    existing_savings = db.query(Savings).filter(Savings.id == savings_id).first()

    if not existing_savings:
        logger.warning(
            "Savings id: %s not found for user_id: %s", savings_id, current_user.id
        )
        return None

    if not is_authorized(existing_savings, current_user):
        logger.warning(
            "Unauthorized update attempt to savings id: %s by user_id: %s",
            savings_id,
            current_user.id,
        )
        raise ValueError("Unauthorized access")

    update_data = saving_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_savings, key, value)

    db.commit()
    db.refresh(existing_savings)

    logger.info("Savings id: %s updated for user_id: %s", savings_id, current_user.id)
    return existing_savings


def delete_saving_service(savings_id: int, current_user: User, db: Session):
    """
    Deleting savings of a user
    """
    logger.info("Deleting savings id: %s for user_id: %s", savings_id, current_user.id)
    existing_savings = db.query(Savings).filter(Savings.id == savings_id).first()

    if not existing_savings:
        logger.warning(
            "Savings id: %s not found for user_id: %s", savings_id, current_user.id
        )
        return None

    if not is_authorized(existing_savings, current_user):
        logger.warning(
            "Unauthorized delete attempt to savings id: %s by user_id: %s",
            savings_id,
            current_user.id,
        )
        raise ValueError("Unauthorized access")

    db.delete(existing_savings)
    db.commit()

    logger.info("Savings id: %s deleted for user_id: %s", savings_id, current_user.id)
    return existing_savings
