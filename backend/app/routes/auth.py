"""
Authentication routes
"""
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.utils.auth import verify_password, create_access_token
from app.utils.user import fetch_by_email, create
from app.db.database import get_db
from app.models import User
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.dependencies.auth import get_current_active_user
from app.utils.rate_limits import limiter

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

    user = fetch_by_email(db, payload.email)

    if not user or not verify_password(payload.password, user.password):
        logger.warning("Failed login attempt for email: %s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("User %s logged in successfully", payload.email)
    token, expire = create_access_token(data={"user_id": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": int((expire - datetime.now(timezone.utc)).total_seconds()),
        "expires_at": expire.isoformat(),
        "user": UserResponse.from_orm(user)
    }


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""

    logger.info("Signup attempt for email: %s", user.email)

    db_user = fetch_by_email(db, user.email)

    if db_user:
        logger.warning("Signup attempt with already registered email: %s", user.email)
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = create(db, user)
    logger.info("User %s created successfully", user.email)
    return new_user
