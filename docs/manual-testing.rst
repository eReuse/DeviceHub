Manual testing
==============

We explain how to do deployment on a regular pc or server, and run commands to try stuff and do some maintenance.
Note that we are not explaining here how to run the test suite.

`Here we explain how to install and run DeviceHub <https://github.com/ereuse/devicehub/#install-and-run>`_.

DeviceHub provides a `folder with scripts <https://github.com/eReuse/DeviceHub/tree/master/ereuse_devicehub/scripts>`_
that are thought to be used in a terminal. Each script explains in a comment how to execute it through the terminal.

- `Create account <https://github.com/eReuse/DeviceHub/blob/master/ereuse_devicehub/scripts/create_account.py>`_ creates
  an account (on the database) and prints it, appending the token.


- `Dummy db <https://github.com/eReuse/DeviceHub/blob/master/ereuse_devicehub/scripts/dummy_db.py>`_ deletes all
  databases defined in the ``settings.py`` and populates the database with a dummy account (a@a.a, 1234) and other
  needed internal accounts, devices, places, pallets and lots. To use it create a python file with the following::

    from ereuse_devicehub import DeviceHub
    from ereuse_devicehub.scripts.dummy_db import DummyDB

    app = DeviceHub()
    DummyDB(app).create_dummy()

  When you run the script you will initialise DeviceHub and the dummy database.

