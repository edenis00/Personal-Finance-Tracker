"""
User Schemas
"""
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserRole(str, Enum):
    """
    Enum for user roles
    """
    user = "user"
    admin = "admin"


class UserCreate(BaseModel):
    """
    Schema for creating a new user
    """
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    role: UserRole = UserRole.user
    profile_img_url: Optional[str] = None


class UserUpdate(BaseModel):
    """
    Schema for updating a user
    """
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    profile_img_url: Optional[str] = None


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
