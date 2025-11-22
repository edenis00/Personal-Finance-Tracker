"""
Authentication utilities
"""
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def hash_password(password: str) -> str:
    """Function to hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Funtion to verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong(password: str) -> bool:
    """Check if the password meets strength requirements."""
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        return False
    return True


def validate_password(password: str) -> None:
    """Validate password strength and raise ValueError if not strong enough."""
    if not is_password_strong(password):
        raise ValueError(
            "Password must be at least 8 characters long, "
            "contain uppercase and lowercase letters, "
            "digits, and special characters."
        )


def create_access_token(data: dict, expires_delta: int=30):
    """create a JWT access token"""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """Decode a JWT access token"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token error: " + str(e))
