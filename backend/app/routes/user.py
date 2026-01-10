"""
User routes
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import User
from app.schema.user import UserResponse, UserUpdate
from app.services.user_service import get_user_service, update_user_service
from app.core.permissions import Permission
from app.schema.base import SuccessResponse
from app.dependencies.rbac import require_permissions as require

router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=SuccessResponse[UserResponse])
def fetch_user(
    current_user: User = Depends(require([Permission.USER_READ])),
    db: Session = Depends(get_db),
):
    """Get a user by ID"""
    logger.info("Fetching user profile for user_id: %s", current_user.id)
    user = get_user_service(db, current_user.id)

    if not user:
        logger.warning("User not found for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    logger.info("User profile retrieved for user_id: %s", current_user.id)
    return SuccessResponse(message="User profile retrieved successfully", data=user)


@router.put("/", response_model=SuccessResponse[UserResponse])
def update_profile(
    user: UserUpdate,
    current_user: User = Depends(require([Permission.USER_WRITE])),
    db: Session = Depends(get_db),
):
    """Update a user"""
    logger.info("Updating user profile for user_id: %s", current_user.id)
    updated_user = update_user_service(db, user, current_user.id)

    if not updated_user:
        logger.warning("User not found for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    logger.info("User profile updated for user_id: %s", current_user.id)
    return SuccessResponse(
        message="User profile updated successfully", data=updated_user
    )
