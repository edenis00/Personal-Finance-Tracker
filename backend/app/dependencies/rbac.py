"""
RBAC (Role-Based Access Control) dependencies
"""
from typing import List
from fastapi import HTTPException, Depends, status
from app.core.permissions import Permission, Role, get_permissions_for_role
from app.dependencies.auth import get_current_user
from app.models.user import User


class RBACChecker:
    """Dependency class to check RBAC permissions"""

    def __init__(self, required_permission: List[Permission]):
        self.required_permission = required_permission
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        """
        Check if the current user has the required permissions
        Args:
            current_user (User): The currently authenticated user
        Raises:
            HTTPException: If the user does not have the required permissions
        returns:
            User object if authorized
        """

        user_role = Role(current_user.role)
        user_permissions = get_permissions_for_role(user_role)

        for permission in self.required_permission:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        
        return current_user

def require_permissions(permissions: List[Permission]):
    """Dependency function to require specific permissions"""
    return RBACChecker(required_permission=permissions)


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency function to require admin role"""
    if current_user.role != Role.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


def require_role(allowed_roles: List[Role]):
    """Dependency function to require specific roles"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = Role(current_user.role)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges"
            )
        return current_user
    return role_checker
