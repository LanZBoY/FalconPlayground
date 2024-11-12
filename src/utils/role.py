import enum


class UserRole(enum.StrEnum):
    ADMIN = "ADMIN"
    NORMAL = "NORMAL"
    GUEST = "GUEST"

class UserRoleGroup:
    PUBLIC = (UserRole.ADMIN, UserRole.NORMAL, UserRole.GUEST, )
    ALL_USER = (UserRole.ADMIN, UserRole.NORMAL,)
    ONLY_ADMIN = (UserRole.ADMIN,)
    