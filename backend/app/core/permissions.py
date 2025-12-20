"""
Role based access control permissions. 
"""
from enum import Enum
from typing import List

class Role(str, Enum):
    """User roles in the system"""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class Permission(str, Enum):
    """System permissions"""
    # User permissions
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"

    # Dasboard permissions
    DASHBOARD_READ = "dashboard:read"
    DASHBOARD_WRITE = "dashboard:write"
    DASHBOARD_DELETE = "dashboard:delete"

    # Expense permissions
    EXPENSE_READ = "expense:read"
    EXPENSE_WRITE = "expense:write"
    EXPENSE_DELETE = "expense:delete"

    # Income permissions
    INCOME_READ = "income:read"
    INCOME_WRITE = "income:write"
    INCOME_DELETE = "income:delete"

    # Savings permissions
    SAVINGS_READ = "savings:read"
    SAVINGS_WRITE = "savings:write"
    SAVINGS_DELETE = "savings:delete"

    # Admin permissions
    ADMIN_READ = "admin:read"
    ADMIN_WRITE = "admin:write"
    ADMIN_DELETE = "admin:delete"


# Role to permissions mapping
ROLE_PERMISSIONS: dict[Role, List[Permission]] = {
    Role.USER: [
        # Users can manage their own data
        Permission.USER_READ,
        Permission.USER_WRITE,

        Permission.DASHBOARD_READ,
        Permission.DASHBOARD_WRITE,
        Permission.DASHBOARD_DELETE,

        Permission.EXPENSE_READ,
        Permission.EXPENSE_WRITE,
        Permission.EXPENSE_DELETE,

        Permission.INCOME_READ,
        Permission.INCOME_WRITE,
        Permission.INCOME_DELETE,

        Permission.SAVINGS_READ,
        Permission.SAVINGS_WRITE,
        Permission.SAVINGS_DELETE,
    ],

    Role.ADMIN: [
        # Admins have all permissions
        Permission.USER_READ,
        Permission.USER_WRITE,
        Permission.USER_DELETE,

        Permission.DASHBOARD_READ,
        Permission.DASHBOARD_WRITE,
        Permission.DASHBOARD_DELETE,

        Permission.EXPENSE_READ,
        Permission.EXPENSE_WRITE,
        Permission.EXPENSE_DELETE,

        Permission.INCOME_READ,
        Permission.INCOME_WRITE,
        Permission.INCOME_DELETE,

        Permission.SAVINGS_READ,
        Permission.SAVINGS_WRITE,
        Permission.SAVINGS_DELETE,

        Permission.ADMIN_READ,
        Permission.ADMIN_WRITE,
        Permission.ADMIN_DELETE,
    ]
}


def get_permissions_for_role(role: Role) -> List[Permission]:
    """Retrieve permissions for a given role"""
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(user_role: Role, permission: Permission) -> bool:
    """Check if a user role has a specific permission"""
    role_permission = get_permissions_for_role(user_role)
    return permission in role_permission
