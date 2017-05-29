API
###

DeviceHub uses `Python-Eve <http://python-eve.org>`_, which exposes a full API.
The system is RESTFUL using HATEOAS, partially extends Schema.org, and uses a very limited (for now)
subset of JSON-LD. We use '@type' to set a type of object and '_id' to identify it.

The main resource are devices. However, you do not perform operations directly against them (there is no ``POST /device``),
as you use an Event to do so (you only ``GET /devices``). For example, to upload information of devices with tests, erasures, etcetera, use
the event ``POST /snapshot`` (:ref:`devices-snapshot`).

Login
=====
To use the API, you will need first to log in with an existing account from the DeviceHub.
Perform ``POST /login`` with the email and password fields filled::

    POST /login
    Content-Type: application/json
    Accept: application/json
    {
        "email": "example@example.com",
        "password": "example"
    }

Upon success, you will be answered with the account object, containing a Token field::

    {
      "databases": [
        "database1",
        "database2"
      ],
      "defaultDatabase": "example_database",
      "password": "sha256 codified password",
      "role": "admin",
      "email": "example@example.com",
      "_id": "149fja02umzl",
      "@type": "Account",
      "token": "Base 64 codified token"
    }

From this moment, any other following operation against the API will require the following HTTP Header:
``Authorization: Basic token``. This is, the word **Basic** followed with a **space** and then the **token**,
obtained from the account object above, **exactly as it is**.

Authenticate requests
---------------------
To explain how to operate with resources like events or devices, we use one as an example: obtaining a particular
device. The template of a request is::

   GET <database>/devices/<deviceId>
   Accept: application/json
   Authorization: Basic <token>

And an example is::

    GET acme/devices/1
    Accept: application/json
    Authorization: Basic myToken

Let's go through the variables:

- ``<database>`` is the name of the database (so called inventory) where you operate.
  You get this value from the ``Account`` object returned from the login. The ``databases`` field contains
  a set of databases the account can operate with, and ``defaultDatabase`` the one a client should use per default.
  DeviceHubClient and the app use ``defaultDatabase`` per default and let the user change the current database using
  a selector. In the example we use the database ``acme``.
- ``<deviceId>`` is the identifier of the device.
- ``<token>`` is the token of the account. We get it, as with ``databases``, from the ``Account`` object after
  performing login.

Filter, order, embed, and project
=================================
Built under Python-Eve, you can always `filter <http://python-eve.org/features.html#filtering>`_::

    https://api.devicetag.io/public/events?where={“@type”: “Snapshot”}

*Exemplifying GET query filtering results. In this case, it obtains all events from the public database of DeviceTag.io that are snapshots.*
*It is using MongoDB syntax, so it supports the majority of filters MongoDB uses.*

`Order <http://python-eve.org/features.html#sorting>`_::

    https://api.devicetag.io/public/devices?sort=_created,-type

*Exemplifying GET query ordering results. In this case, it obtains all devices from the public database of DeviceTag.io,*
*sorting them by the fields of byUser (ascending) and byOrganization (descending). It is using native Python syntax.*

`Embed <http://python-eve.org/features.html#embedded-resource-serialization>`_::

    https://api.devicetag.io/public/devices?embedded={“byUser”:1, “events”:1}

*Exemplifying GET query embedding results. In this case, it obtains all devices from the public database of DeviceTag.io,*
*and embeds the user object, and a list with all the objects of all events, using MongoDB syntax.*

And `project <http://python-eve.org/features.html#projections>`_::

    https://api.devicetag.io/public/places?projection={“byUser”:0}

*Exemplifying GET query with projection definition. In this case, it obtains all places from the public database of DeviceTag.io;*
*however, it does not retrieve the field byUser. It uses MongoDB syntax.*

Finally, we can join everything::

    https://api.devicetag.io/public/devices?where={“type”: “TFT”}&sort=[(“labelId”,1)]

*Exemplifying GET query combining different operations. In this case, it obtains all devices from the public*
*database of DeviceTag.io that are TFT (sub type of monitors) and it sorts them by labelId (ascending).*

The Schema
==========
The Schema endpoint defines all the resource endpoints, detailing how values should be. The Schema is a superset of
the `eve's schema <http://python-eve.org/config.html#schema>`_, as we define more schema rules. The Schema is
internally used by DeviceHub to validate fields and by the web app to configure several parameters and generate
the forms.

To retrieve the schema:

 1. **Login**, as DeviceHub only sends you the portion of the schema the user can interact with. If you do not login you
    can still get the schema, but you may not see it fully.
 2. ``GET /schema``.

You can `try it and see it in the browser <https://api.devicetag.io/schema>`_.

You can also do ``GET /schema/devices_snapshot`` for any endpoint. Note that resource names with *:* are changed for
*_* to make it URL valid. See more `in eve's documentation <http://python-eve.org/features.html#the-schema-endpoint>`_.

Original rules from Python-eve are explained `here <http://python-eve.org/config.html#schema>`_, and the ones we add
are methods of the class: :class:`ereuse_devicehub.validation.validation.DeviceHubValidator`. Any method starting with
``_validate_`` is a validation rule, except the following cases:

 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_sink`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_description`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_short`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_unitCode`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_doc`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_uid`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_externalSynthetic`
 - :meth:`ereuse_devicehub.validation.validation.DeviceHubValidator._validate_allowed_description`



In the following section you have a more human representation of the schema (it is not updated):

API Endpoints
-------------
The following list describes the details of every endpoint in DeviceHub:


.. toctree::
   :maxdepth: 4

   other-endpoints
   api-endpoints


Errors
======
We are working for all errors to be like the following:

Errors extend from the Error class in Hydra and are represented as follows: the ``@type`` field describing the type of class
or error, a ``title`` field representing a translated human title, and a ``description`` representing a translated human
description of the error::

    HTTP 401 <http://www.ereuse.org/onthology/UnauthorizedToUseDatabase.jsonld>;
    rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"
    {
      '_error': {
          'message': 'message',
          'code': 401,
          '@type': UnauthorizedToUseDatab}ase
      }
      '_status': 'ERR'
    }

As you can see, the server sets the most specific HTTP status code.

Examples
========
You have some real example to catch-on fast.

Device
------
The following example illustrates how to retreive a resource, like a device.
And the result::

    {
      "components": [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9"
      ],
      "forceCreation": false,
      "hid": "dell_inc-5yb864j-optiplex_760",
      "_created": "2016-04-11T18:30:50",
      "_id": "1",
      "_updated": "2016-04-11T18:30:50",
      "serialNumber": "5YB864J",
      "model": "OptiPlex 760",
      "@type": "Computer",
      "isUidSecured": true,
      "_links": {
        "self": {
          "title": "Device",
          "href": "db1/devices/1"
        },
        "collection": {
          "title": "devices",
          "href": "db1/devices"
        },
        "parent": {
          "title": "home",
          "href": "/"
        }
      },
      "type": "Microtower",
      "icon": "devices/icons/Microtower.svg",
      "labelId": "D01151",
      "public": false,
      "manufacturer": "Dell Inc.",
      "_etag": "651e535c9dcddacb26d8bf5673075a811f735d58"
    }

Collection of events
--------------------
The following example shows two things, first the structure when GET collection of resources, and then one event::

    {
      "_links": {
        "self": {
          "title": "events",
          "href": "db1/events"
        },
        "parent": {
          "title": "home",
          "href": "/"
        },
        "last": {
          "title": "last page",
          "href": "db1/events?page=5"
        },
        "next": {
          "title": "next page",
          "href": "db1/events?page=2"
        }
      },
      "_meta": {
        "total": 125,
        "max_results": 30,
        "page": 1
      },
      "_items": [
        {
          "device": "424",
          "parent": "422",
          "_created": "2016-06-09T09:12:28",
          "_id": "575932fc7a993d03216f6f5e",
          "_updated": "2016-06-09T09:12:28",
          "secured": false,
          "lifetime": 1121,
          "status": "Completed: read failure",
          "incidence": false,
          "@type": "TestHardDrive",
          "error": true,
          "type": "Short offline",
          "_links": {
            "self": {
              "title": "Event",
              "href": "db1/events/575932fc7a993d03216f6f5e"
            }
          },
          "firstError": 18448359,
          "byUser": "5759278b7a993d03216f6ee3"
        }
      ]
    }

Creating a device
=================
To create a device you need to create (to post) an event. In DeviceHub, you usually don't work directly through devices,
but perform events on them –we feed the traceability log with events.

To create a device you do it through the event :ref:`devices-Register`. Register internally POST a device, so
``Register`` is only **performed once per device**. ``Register`` is used when creating a device manually through
DeviceHubClient, but not when using Workbench or the App. This is because in the Workbench, for example, we
collect information of the device; we don't know if the device existed before,
we only want to update the information DeviceHub has from such device (for example, if a component changed). Because
of this, in this case we use the event :ref:`devices-Snapshot`. ``Snapshot`` updates the information a DeviceHub
has from the device, performing internally ``Register`` and other events if needed.


To just create a device, like a placeholder, use ``Register`` (and avoid two events). To update information of
a device, including benchmarks, erasures... and possibly a Register, use ``Snapshot``.

See in :ref:`event` a definition for ``Register`` and ``Snapshot``.

Snapshot
--------
An example of a Snapshot is::

    POST <database>/events/devices/snapshot
    Content-type: application/json
    Accept: application/json
    Authorization: Basic <token>

You have an example of the body of a Snapshot request
`here <https://github.com/eReuse/DeviceHub/blob/master/ereuse_devicehub/tests/fixtures/snapshot/8a1.json>`_.

DeviceHub requires the device in the ``device`` property (not its components) to generate a HID.
This is, the computer has a S/N, model and manufacturer. Otherwise the computer is rejected (``HTTP 422``).

.. todo:: Show response for 422 NeedsId

A device can be accepted even if some rules are broken. If such case, DeviceHub will response with information about
the broken rules. As an example (see the ``ruling`` property)::

   HTTP 201
   Content-Type: application-json
   {
      "device": "1",
      "_id": "xxxxxxxxxxxxxxxxx",
      "@type": "devices:Snapshot",
      "components": [],
      "events": [],
      "ruling": {
         "status": "error",
         "label": "",
         "description": "",
         "color": ""
      }
      "_status": "OK"
      "_created": "1492-01-01T00:00:00",
      "_updated": "1492-01-01T00:00:00",
   }

.. todo:: rules are an unimplemented proposal that can be changed

Deleting resources
==================
Deleting resources (events or devices specifically) is against traceability. What is the credibility of a log if you
can modify it and delete it? So, we usually don't let deleting anything. However, as an exception, we let deleting
an event or device if:

- It has been created in lesser than X seconds (per default, 10 minutes). We only want to allow deleting for
  correcting human mistakes (*"I forgot to add a field to that event!"*).
- In the case of deleting an event:

  - It is the last event performed on all of the devices it affects, unless it is a Snapshot and all the events
    after it were generated by the Snapshot.
  - It is not a Migrate.
- In the case of deleting a device:

  - It does not have a Migrate (Migrate form or Migrate to, it does not matter).

Note that Migrate are tough events involving different databases and organizations and, until a course of action is
defined we will just not allow it to be erased.

Note that although it is redundant for this operation, the system it checks too that the device is
in the current database (not Migrated to another DB). And finally, if you look at
:py:func:`ereuse_devicehub.hooks.hooks` you can see the hooks that check those conditions assigned on
``app.on_delete_item`` and ``app.on_PRE_delete``.
