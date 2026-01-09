"""
Authentication routes
"""

import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.utils.auth import login_service, UserNotFoundError, signup_service
from app.db.database import get_db
from app.models import User
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.dependencies.auth import get_current_active_user
from app.utils.rate_limits import limiter
from app.schema.base import SuccessResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user"""
    return current_user


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")  # Rate limiting: 5 requests per minute
def login(request: Request, payload: UserLogin, db: Session = Depends(get_db)):
    """User Login route"""

    logger.info("Login attempt for email: %s", payload.email)
    try:
        user, token, expire = login_service(payload, db)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": int((expire - datetime.now(timezone.utc)).total_seconds()),
            "expires_at": expire.isoformat(),
            "user": UserResponse.from_orm(user),
        }
    except ValueError as e:
        if "password" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to login in user due to: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post(
    "/signup",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")  # Rate limiting: 3 requests per minute
def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""

    logger.info("Signup attempt for email: %s", user.email)
    try:
        new_user = signup_service(user, db)
        logger.info("User %s created successfully", user.email)
        return SuccessResponse(message="User created successfully", data=new_user)
    except ValueError as e:
        if "already registered" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to sign in user due to: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
