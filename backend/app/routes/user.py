"""
User routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.user import UserResponse, UserCreate, UserUpdate
from app.utils.user import fetch, fetch_all, fetch_by_email, create, update, delete

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/{user_id}", response_model=UserResponse)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    user = fetch(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/", response_model=list[UserResponse])
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    users = fetch_all(db, skip=skip, limit=limit)

    return users


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    db_user = fetch_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create(db, user)

    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user"""
    updated_user = update(db, user, user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    deleted_user = delete(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted successfully"}
