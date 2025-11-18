"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth import verify_password, create_access_token, is_password_strong, validate_password
from app.utils.user import fetch_by_email, create
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.db.database import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """User Login route"""

    db_user = fetch_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found"
        )

    if is_password_strong(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak"
        )

    if validate_password(user.password):
        raise HTTPException(    
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not meet criteria"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""

    db_user = fetch_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_user = create(db, user)

    return new_user
