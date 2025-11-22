"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth import verify_password, create_access_token
from app.utils.user import fetch_by_email, create
from app.db.database import get_db
from app.schema.user import UserCreate, UserResponse, UserLogin


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

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_access_token(data={"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""

    db_user = fetch_by_email(db, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create(db, user)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        phone_number=new_user.phone_number,
        role=new_user.role,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        profile_img_url=new_user.profile_img_url,
    )
