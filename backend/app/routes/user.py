"""
User routes
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import User
from app.schema.user import UserResponse, UserUpdate
from app.utils.user import fetch, update, fetch_all, delete
from app.core.permissions import Permission
from app.schema.base import SuccessResponse
from app.dependencies.rbac import require_permissions as require

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

logger = logging.getLogger(__name__)

@router.get("/", response_model=SuccessResponse[UserResponse])
def fetch_user(
    current_user: User = Depends(
        require([Permission.USER_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get a user by ID"""
    logging.info("Fetching user profile for user_id: %s", current_user.id)
    user = fetch(db, current_user.id)

    if not user:
        logging.warning("User not found for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
    )

    logging.info("User profile retrieved for user_id: %s", current_user.id)
    return SuccessResponse(
        message="User profile retrieved successfully",
        data=user
    )


@router.put("/", response_model=SuccessResponse[UserResponse])
def update_profile(
    user: UserUpdate,
    current_user: User = Depends(
        require([Permission.USER_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """Update a user"""
    logging.info("Updating user profile for user_id: %s", current_user.id)
    updated_user = update(db, user, current_user.id)

    if not updated_user:
        logging.warning("User not found for user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User profile updated for user_id: %s", current_user.id)
    return SuccessResponse(
        message="User profile updated successfully",
        data=updated_user
    )



# admin routes

@router.get("/", response_model=SuccessResponse[list[UserResponse]])
def fetch_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""

    logging.info("Fetching users list by admin user_id: %s", current_user.id)
    users = fetch_all(db, skip=skip, limit=limit)

    if not users:
        logging.warning("No users found by admin user_id: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )

    logging.info("Users list retrieved by admin user_id: %s", current_user.id)
    return SuccessResponse(
        message="Users retrieved successfully",
        data=users
    )


@router.get("/{user_id}", response_model=SuccessResponse[UserResponse])
def fetch_user_by_id(
    user_id: int,
    current_user: User = Depends(
        require([Permission.ADMIN_READ])
    ),
    db: Session = Depends(get_db)
):
    """Get a user by ID for admins"""

    logging.info("Fetching user_id: %s by admin user_id: %s", user_id, current_user.id)
    user = fetch(db, user_id)

    if not user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User_id: %s retrieved by admin user_id: %s", user_id, current_user.id)
    return SuccessResponse(
        message="User retrieved successfully",
        data=user
    )


@router.put("/{user_id}", response_model=SuccessResponse[UserResponse])
def update_user_by_id(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(
        require([Permission.ADMIN_WRITE])
    ),
    db: Session = Depends(get_db)
):
    """Update a user for admins"""

    logging.info("Updating user_id: %s by admin user_id: %s", user_id, current_user.id)
    updated_user = update(db, user, user_id)

    if not updated_user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User_id: %s updated by admin user_id: %s", user_id, current_user.id)
    return SuccessResponse(
        message="User updated successfully",
        data = updated_user
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(
        require([Permission.ADMIN_DELETE])
    ),
    db: Session = Depends(get_db)):
    """Delete a user for admins"""

    logging.info("Deleting user_id: %s by admin user_id: %s", user_id, current_user.id)
    deleted_user = delete(db, user_id)

    if not deleted_user:
        logging.warning("User_id: %s not found by admin user_id: %s", user_id, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logging.info("User_id: %s deleted by admin user_id: %s", user_id, current_user.id)
    return {"detail": "User deleted successfully"}