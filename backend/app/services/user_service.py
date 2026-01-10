"""
User Service
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user import UserCreate, UserUpdate
from app.utils.auth import hash_password


def get_user_service(db: Session, user_id: int):
    """Fetch a user by id"""
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_all_users_service(db: Session, skip: int = 0, limit: int = 100):
    """Fetch all users with pagination"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


def get_user_by_email_service(db: Session, email: str):
    """Fetch a user by email"""
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user_service(db: Session, user: UserCreate):
    """Create a new user"""

    if get_user_by_email_service(db, user.email):
        raise ValueError("Email already registered")

    hashed_password = hash_password(user.password) if user.password else None

    user_data = user.model_dump(exclude={"password"})
    user_data["password"] = hashed_password

    new_user = User(**user_data)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise e

    return new_user


def update_user_service(db: Session, user: UserUpdate, user_id: int):
    """Update user"""

    update_user = db.query(User).filter(User.id == user_id).first()

    if not update_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(update_user, key, value)

    try:
        db.commit()
        db.refresh(update_user)
    except Exception:
        db.rollback()
        raise

    return update_user


def delete_user_service(db: Session, user_id: int):
    """Delete user"""
    delete_user = db.query(User).filter(User.id == user_id).first()
    if not delete_user:
        return None

    db.delete(delete_user)
    db.commit()

    return delete_user
