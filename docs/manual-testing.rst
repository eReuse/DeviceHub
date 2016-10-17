Manual testing
==============

We explain how to do deployment on a regular pc or server, and run commands to try stuff and do some maintenance.
Note that we are not explaining here how to run the test suite.

DeviceHub provides a `folder with scripts <https://github.com/eReuse/DeviceHub/tree/modules/ereuse_devicehub/scripts>`_
that are thought to be used in a terminal. Each script explains in a comment how to execute it through the terminal.

- `Create account <https://github.com/eReuse/DeviceHub/blob/modules/ereuse_devicehub/scripts/create_account.py>`_ creates
an account (on the database) and prints it, appending the token.


`Dummy db <https://github.com/eReuse/DeviceHub/blob/modules/ereuse_devicehub/scripts/dummy_db.py>`_ populates the database
with dummy devices and places, so it is easy to test. To use it, as it says in the comments, create a python file with the following:

    from ereuse_devicehub import DeviceHub
    from ereuse_devicehub.scripts.dummy_db import DummyDB
    app = DeviceHub()
    d = DummyDB(app)
    d.create_dummy_devices()

When you run the script you will initialise DeviceHub and the dummy database.


DeviceHub has extensions that can be 'plugged-in' like regular
`Flask extensions <http://flask.pocoo.org/docs/0.11/extensions/>`_,
like `DeviceHubProject <https://github.com/ereuse/devicehub-project>`_. They usually extend 'dummy_db' and add some other scripts,
so it is better to use them. If we want to use DeviceHubProject dummy db, we adapt the above example to be like this:

    from ereuse_devicehub import DeviceHub
    from devicehub_project import DeviceHubProject
    from devicehub_project.scripts.dummy_db import DeviceHubProjectDummyDB
    app = DeviceHub()
    DeviceHubProject(app)
    d = DeviceHubProjectDummyDB(app)
    d.create_dummy_devices()

If you save this file, for example, as 'my_script.py', execute in a terminal 'python my_script.py'.