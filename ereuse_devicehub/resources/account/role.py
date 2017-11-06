class Role:
    """
    Roles specify what users can do generally.
    Locations alter what users can do. Locations permissions > roles. Admins don't get affected by location perms.
    Roles are ordered hierarchically. This means that an admin role has the same permissions as a user, and more.
    The gradient is:
    MACHINE < USER < SUPER_MACHINE < ADMIN < SUPERUSER

    We can use operators to compare between roles. For example BASIC < AMATEUR == True
    """
    MACHINE = 'm'
    """Accounts used by services accessing DeviceHub"""
    USER = 'u'
    """Regular user."""
    SUPERMACHINE = 'sm'
    """Machines with more access"""
    ADMIN = 'a'
    """Managers of the devicehub, in general."""
    SUPERUSER = 'su'
    """Total system control"""

    ROLES = MACHINE, USER, SUPERMACHINE, ADMIN, SUPERUSER
    MANAGERS = ADMIN, SUPERUSER
    MACHINES = MACHINE, SUPERMACHINE

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

    def __str__(self) -> str:
        return self.role
