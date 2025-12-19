from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ResponseBase(BaseModel):
    """Response base schema"""
    success: bool
    message: str


class SuccessResponse(ResponseBase, Generic[T]):
    """Success response schema"""
    success: bool = True
    message: str = "success"
    data: T


class ErrorResponse(ResponseBase, Generic[T]):
    """Error response schema"""
    success: bool = False
    message: str
    errors: Optional[dict] = None