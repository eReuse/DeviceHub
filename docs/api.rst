API
===

DeviceHub uses `Python-Eve <http://python-eve.org>`_, which exposes a full API.
The system is RESTFUL using HATEOAS, partially extends Schema.org, and uses a very limited (for now)
subset of JSON-LD. We use '@type' to set a type of object and '_id' to identify it.

In DeviceHub there are four main resources:

- Device
- Event
- Place
- Account

The main resource are devices. However, you do not perform operations directly against them (there is no ``POST /device``),
as you use an Event to do so (you only ``GET /devices``). For example, to upload information of devices with tests, erasures, etcetera, use
the event ``POST /snapshot`` (:ref:`snapshot`).

Login
-----
To use the API, you will need first to log in with an existing account from the DeviceHub.
Perform ``POST /login`` with the email and password fields filled::

    POST /login
    Content-Type: application/json
    {
        "email": "example@example.com",
        "password": "example"
    }

Upon success, you will be answered with the account object, containing a Token field::

    {
      "databases": [
        "example_database",
        "example_database_2"
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
``Authorization: Basic token``.

Working with devices
____________________


Filter, order, embed, and project
_________________________________
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


API Endpoints
_____________
The following list describes the details of every endpoint in DeviceHub:

.. toctree::
   :maxdepth: 4

   api-endpoints

Errors
______
We are working for all errors to be like the following:

Errors extend from the Error class in Hydra and are represented as follows: the ``@type`` field describing the type of class
or error, a ``title`` field representing a translated human title, and a ``description`` representing a translated human
description of the error::

    HTTP 401 <http://www.ereuse.org/onthology/UnauthorizedToUseDatabase.jsonld>;
    rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"
    {
    “@type”: “UnauthorizedToUseDatabase”,
    “title”: “Unauthorized to use the database db1”, “description”: “User has no access to this database.”
    }
As you can see, the server sets the most specific HTTP status code.

Examples
________
You have some real example to catch-on fast.

Device
^^^^^^
The following example illustrates how to retreive a resource, like a device. The request is::

    GET /devices/1
    Accept: application/json
    Authorization: Basic myToken

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
^^^^^^^^^^^^^^^^^^^^
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

