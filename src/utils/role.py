import enum


class UserRole(enum.StrEnum):
    ADMIN = "ADMIN"
    NORMAL = "NORMAL"

class UserRoleGroup:

    ALL_USER = (UserRole.ADMIN, UserRole.NORMAL,)
    ONLY_ADMIN = (UserRole.ADMIN,)
    