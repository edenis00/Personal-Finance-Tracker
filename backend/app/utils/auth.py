"""
Authentication utilities
"""
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60


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
            "sub": str(data.get("user_id"))
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
                detail="Inavlid token: Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inavlid token: Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from e
