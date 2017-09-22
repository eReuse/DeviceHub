Authorization
=============

Here we explain how permissions are handled in DeviceHub.
To learn how to authenticate requests go to :ref:`authenticate-requests`.

There are three types of permissions in DeviceHub:

Roles
-----
Define the type of user and ultimately which broad actions it can do.

We can group roles in 3:

- User role, automatically given to regular users.
- admin and superuser role, for those users with the power to create users or change passwords.
- Machine roles, to give access to machine agents.

Go to the class :class:`ereuse_devicehub.resources.account.role.Role` to get more info.

Database permissions
--------------------
Control which databases (or inventories, as they are the same) users can access to and what they can do in there.

An user usually can fully access to its own database, and only to the shared groups of the other databases (which
we call ``partial access``).

Database permissions are set in the user's account,
in :attr:`ereuse_devicehub.resources.account.settings.Account.databases`. A default database is usually
used by app clients to show it as default when the user opens the app, and it is set in
:attr:`ereuse_devicehub.resources.account.settings.Account.defaultDatabase`.

Database permissions are listed in :mod:`ereuse_devicehub.security.perms`.

Group permissions
-----------------
Permissions that users set to their groups when *sharing* them to others. For example,
an user can share a lot to specific users, setting a ``READ`` permission so they cannot modify its contents.
This mimics what Dropbox of Google Drive do with sharing folders, but with groups.

Group permissions are set in groups and devices, in
:attr:`ereuse_devicehub.resources.group.settings.Group.perms` and
:attr:`ereuse_devicehub.resources.device.settings.Device.perms`.

The permissions are listed in :py:mod:`ereuse_devicehub.security.perms`.

Adding and removing permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Users are only allowed to set and remove permissions on groups. Devices can only inherit permissions from groups.

When a permission is set to a group, this is inherited for all descendants, overriding the permission the
descendants had for that account (if you are setting the permission ``READ`` and some descendants had the permission
``WRITE`` for that account, they will loose ``WRITE`` and get ``READ``). This does not affect permissions descendants
had for *other* accounts.

When a permission is removed from a group, this is inherited to all its descendants in the same way.

Adding and removing resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When adding a resource to a group that is shared to an user, the resource and all its descendants will inherit
the new permissions.

When removing a resource from a group, they will loose all permissions that were not *explicitly
set* to them (see next paragraph).

Explicit permissions
~~~~~~~~~~~~~~~~~~~~
When setting a permission to a group, the system remembers which group the user **explicitly** set
the permission to, to discriminate those groups that inherit the permission. This is set in the
field :attr:`ereuse_devicehub.resources.group.settings.Group.sharedWith` in the group and then
materialized in the field :attr:`ereuse_devicehub.resources.account.settings.Account.shared` in the
account. There are three purposes for this:

- User is granted automatically ``partial access`` to a database when someone shares a group from it,
  and the user will loose access to that database when it looses access to those **explicit** groups.
- Clients and the system can know which databases and groups the user has access to by looking
  to ``databases`` and ``shared`` account fields.
- When removing resources from a group, they loose all their permissions recursively except those that were
  explicitly set. For example:

  1. Given an user A, user B, group 1, group 2 and group 3. We are working with a database user A owns and user B
     cannot access to.
  2. User A sets ``WRITE`` permission to user B in group 1. User B now has ``partial access`` to the database A owns.
  3. User A sets ``READ`` permission to user B in group 3. Both group 1 and 3 now have explicit access for user B.
  4. User A creates a group 2 (without setting permissions).
  5. User A adds group 3 into group 2. Group 3 inherits all permissions from group 2; as group 2 does not have
     permissions set, group 3 inherits hing. Group 3 keeps remaining its ``READ`` permission set in step 3.
  6. User A adds group 2 into group 1. Group 2 and group 3 inherits all permissions from group 1, which is
     ``READ`` for user B. As you can note, group 3 changed its permission from ``READ`` to ``WRITE``.
  7. We remove group 2 from group 1. Group 2 looses ``READ`` permission, and although group 3 should loose it too,
     as it was explicitly set in step 3, it keeps the permission. Note that it keeps ``WRITE`` and not ``READ``.

Inheriting groups and permissions for components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Devices that are added into other devices (e.g. components) copy-paste all the groups and permissions of the parent,
  loosing any access they had before. From that point, they will inherit all permissions and groups from the parent.
- When removing components, they won't loose any group or permissions they had with the parents, but from that moment
  on they are *on their own* –they won't receive any new group or permission from the parent.

Accessing events
~~~~~~~~~~~~~~~~

Events are closely tied to the devices they represent; you can't set a permission to an event per se and they
inherit groups and permissions of the devices they represent.

To access an event you need to be able to access to **any** of its devices or components.

As version 0.6, you can create ``Reserve`` events when you don't have full access to an inventory.
To create them you need to be able to access to all of the devices you want to reserve. Other events will
be added in the future.
