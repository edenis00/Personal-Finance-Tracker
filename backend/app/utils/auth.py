"""
Authentication utilities
"""

import logging
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.models import User
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class UserNotFoundError(Exception):
    pass


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def login_service(user_login, db: Session):
    """
    Service for login functionalities
    """
    try:
        user = db.query(User).filter(User.email == user_login.email).first()
        if not user:
            logger.warning("Data for user: %s not found", user_login.email)
            raise UserNotFoundError("User does not exist")

        if not verify_password(user_login.password, user.password):
            logger.warning("Invalid password for user: %s", user_login.email)
            raise ValueError("Invalid Password")

        logger.info("User %s logged in successfully", user_login.email)
        token, expire = create_access_token(data={"user_id": str(user.id)})
        return user, token, expire
    except Exception as e:
        logger.error("Failed to login user %s due to: %s", user_login.email, str(e))
        raise


def signup_service(new_user, db: Session):
    """
    Signup service for creating new users

    :param new_user: Description
    :param db: Description
    """
    try:
        user = db.query(User).filter(User.email == new_user.email).first()
        if user:
            logger.warning(
                "Signup attempt with already registered email: %s", user.email
            )
            raise ValueError("Email is already registered")

        hashed_password = (
            hash_password(new_user.password) if new_user.password else None
        )

        user_data = new_user.model_dump()
        user_data["password"] = hashed_password

        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        logger.error("Failed to create user due to: %s", e)
        raise e


def hash_password(password: str) -> str:
    """Function to hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Funtion to verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong(password: str) -> bool:
    """Check if the password meets strength requirements."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        raise ValueError("Password must contain at least one special character")
    return True


def validate_password(password: str) -> None:
    """Validate password strength and raise ValueError if not strong enough."""
    if not is_password_strong(password):
        raise ValueError(
            "Password must be at least 8 characters long, "
            "contain uppercase and lowercase letters, "
            "digits, and special characters."
        )


def create_access_token(data: dict):
    """create a JWT access token"""

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "sub": str(data.get("user_id")),
        }
    )

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def decode_access_token(token: str):
    """Decode a JWT access token"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
