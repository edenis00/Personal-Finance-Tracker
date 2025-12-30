"""
User Schemas
"""
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime


class UserRole(str, Enum):
    """
    Enum for user roles
    """
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserCreate(BaseModel):
    """
    Schema for creating a new user
    """
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    role: UserRole = UserRole.USER
    profile_img_url: Optional[str] = None
    balance: float

    @field_validator("balance")
    @classmethod
    def validate_balance(cls, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        return value

class UserUpdate(BaseModel):
    """
    Schema for updating a user
    """
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    profile_img_url: Optional[str] = None
    balance: float

    @field_validator("balance")
    @classmethod
    def validate_balance(cls, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        return value


class AdminUserUpdate(BaseModel):
    """Schema for admin updating a user"""
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserResponse(BaseModel):
    """
    Schema for user response
    """
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    role: UserRole
    balance: float
    is_active: bool
    is_verified: bool
    profile_img_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email: EmailStr
    password: str
