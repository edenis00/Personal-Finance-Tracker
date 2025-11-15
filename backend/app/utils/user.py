"""
User utils
"""
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schema.user import UserCreate


def fetch(db: Session, user_id: int):
    """Fetch a user by id"""
    user = db.query(User).filter(User.id == user_id).first()
    return user


def fetch_all(db: Session, skip: int = 0, limit: int = 100):
    """Fetch all users with pagination"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


def fetch_by_email(db: Session, email: str):
    """Fetch a user by email"""
    user = db.query(User).filter(User.email == email).first()
    return user


def create(db: Session, user: UserCreate):
    """Create a new user"""
    new_user = User(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        profile_img_url=user.profile_img_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update(db: Session, user: UserCreate, user_id: int):
    """Update user"""
    update_user  = db.query(User).filter(User.id == user_id).first()
    if not update_user:
        return None

    update_user.email = user.email
    update_user.first_name = user.first_name
    update_user.last_name = user.last_name
    update_user.phone_number = user.phone_number
    update_user.role = user.role
    update_user.is_active = user.is_active
    update_user.is_verified = user.is_verified
    update_user.profile_img_url = user.profile_img_url

    db.commit()
    db.refresh(update_user)

    return update_user


def delete(db: Session, user_id: int):
    """Delete user"""
    delete_user = db.query(User).filter(User.id == user_id).first()
    if not delete_user:
        return None

    db.delete(delete_user)
    db.commit()

    return delete_user
