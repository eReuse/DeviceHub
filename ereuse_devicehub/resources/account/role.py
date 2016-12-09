class Role:
    """
    Roles specify what users can do generally.
    Locations alter what users can do. Locations permissions > roles. Admins don't get affected by location perms.
    Roles are ordered hierarchically. This means that an amateur role has the same permissions as a basic, and more.
    An employee can do the same as an amateur, and more.
    The gradient is:
    BASIC < AMATEUR < EMPLOYEE < ADMIN < SUPERUSER

    We can use operators to compare between roles. For example BASIC < AMATEUR == True
    """
    BASIC = 'basic'
    """Most basic user. Cannot do anything (except its account). Useful for external people."""
    AMATEUR = 'amateur'
    """Can create devices, however can just see and edit the ones it created. Events are restricted."""
    EMPLOYEE = 'employee'
    """Technicians. Full spectre of operations. Can interact with devices of others."""
    ADMIN = 'admin'
    """worker role + manage other users (except superusers). No location restrictions. Can see analytics."""
    SUPERUSER = 'superuser'
    """admin + they don't appear as public users, and they can manage other superusers. See all databases."""
    ROLES = BASIC, AMATEUR, EMPLOYEE, ADMIN, SUPERUSER
    """In grading order (BASIC < AMATEUR)"""
    MANAGERS = ADMIN, SUPERUSER

    def __init__(self, representation):
        if representation not in self.ROLES:
            raise TypeError(representation + ' is not a role.')
        self.role = representation

    def is_manager(self):
        return self.role in self.MANAGERS

    def has_role(self, roles: set):
        return self.role in roles

    def __lt__(self, other):
        if isinstance(other, Role):
            return self.ROLES.index(self.role) < self.ROLES.index(other.role)
        elif isinstance(other, str):
            return self.ROLES.index(self.role) < self.ROLES.index(other)
        else:
            raise NotImplemented

    def __le__(self, other):
        if isinstance(other, Role):
            return self.ROLES.index(self.role) <= self.ROLES.index(other.role)
        elif isinstance(other, str):
            return self.ROLES.index(self.role) <= self.ROLES.index(other)
        else:
            raise NotImplemented

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        if isinstance(other, Role):
            return self.role == other.role
        elif isinstance(other, str):
            return self.role == other
        else:
            raise NotImplemented

    def __hash__(self):
        return self.role.__hash__()
