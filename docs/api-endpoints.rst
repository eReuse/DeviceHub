API
===
.. _Account:

Account
--------------------
.. http:get:: (string:database)/accounts



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string _id:
   :>jsonarr email \*email: Unique: True
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string password: Doc: Users can only see their own passwords.
   :>jsonarr string name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr boolean isOrganization: 
   :>jsonarr string organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr string \*@type: Allowed: {'Account'}
   :>jsonarr string role: Doc: See the Roles section to get more info., Allowed: {'superuser', 'basic', 'amateur', 'employee', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser')
   :>jsonarr list fingerprints: Read only: True
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr boolean active: Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter., Default: True
   :>jsonarr boolean blocked: Description: As a manager, you need to specifically accept the user by unblocking it's account., Default: True, Roles with writing permission: ('admin', 'superuser')
   :>jsonarr string description: Description: Full long description
   :>jsonarr databases \*databases: Roles with writing permission: ('admin', 'superuser')
   :>jsonarr string defaultDatabase: Roles with writing permission: ('admin', 'superuser')
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:post:: (string:database)/accounts



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json email \*email: Unique: True
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :>json email \*email: Unique: True
   :<json string password: Doc: Users can only see their own passwords.
   :<json string name: Description: The name of an account, if it is a person or an organization.
   :>json string name: Description: The name of an account, if it is a person or an organization.
   :<json boolean isOrganization: 
   :>json boolean isOrganization: 
   :<json string organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json string \*@type: Allowed: {'Account'}
   :<json string role: Doc: See the Roles section to get more info., Allowed: {'superuser', 'basic', 'amateur', 'employee', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser')
   :<json string publicKey: Write only: True
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'Account'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string role: Doc: See the Roles section to get more info., Allowed: {'superuser', 'basic', 'amateur', 'employee', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser')
   :<json boolean active: Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter., Default: True
   :>json boolean active: Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter., Default: True
   :<json boolean blocked: Description: As a manager, you need to specifically accept the user by unblocking it's account., Default: True, Roles with writing permission: ('admin', 'superuser')
   :<json string description: Description: Full long description
   :<json databases \*databases: Roles with writing permission: ('admin', 'superuser')
   :>json string description: Description: Full long description
   :>json databases \*databases: Roles with writing permission: ('admin', 'superuser')
   :<json string defaultDatabase: Roles with writing permission: ('admin', 'superuser')
   :>json string defaultDatabase: Roles with writing permission: ('admin', 'superuser')
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:patch:: (string:database)/accounts/(regex("[a-f0-9]{24}"):_id)



    Additional Lookup: (string:database)/accounts/*(regex("[^@]+@[^@]+\.[^@]+"):email)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string label: Description: A short, descriptive title
   :>json email \*email: Unique: True
   :>json string name: Description: The name of an account, if it is a person or an organization.
   :>json boolean isOrganization: 
   :>json string organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string \*@type: Allowed: {'Account'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string role: Doc: See the Roles section to get more info., Allowed: {'superuser', 'basic', 'amateur', 'employee', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser')
   :>json boolean active: Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter., Default: True
   :>json string description: Description: Full long description
   :>json databases \*databases: Roles with writing permission: ('admin', 'superuser')
   :>json string defaultDatabase: Roles with writing permission: ('admin', 'superuser')
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/accounts/(regex("[a-f0-9]{24}"):_id)



    Additional Lookup: (string:database)/accounts/*(regex("[^@]+@[^@]+\.[^@]+"):email)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/accounts/(regex("[a-f0-9]{24}"):_id)



    Additional Lookup: (string:database)/accounts/*(regex("[^@]+@[^@]+\.[^@]+"):email)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json email \*email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json string password: Doc: Users can only see their own passwords.
   :>json string name: Description: The name of an account, if it is a person or an organization.
   :>json boolean isOrganization: 
   :>json string organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string \*@type: Allowed: {'Account'}
   :>json string role: Doc: See the Roles section to get more info., Allowed: {'superuser', 'basic', 'amateur', 'employee', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser')
   :>json list fingerprints: Read only: True
   :>json url sameAs: Read only: True, Unique: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json boolean active: Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter., Default: True
   :>json boolean blocked: Description: As a manager, you need to specifically accept the user by unblocking it's account., Default: True, Roles with writing permission: ('admin', 'superuser')
   :>json string description: Description: Full long description
   :>json databases \*databases: Roles with writing permission: ('admin', 'superuser')
   :>json string defaultDatabase: Roles with writing permission: ('admin', 'superuser')
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:post:: (string:database)/login



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :<json string email: The email of the account.
   :<json string password: The password of the account.
   :>json string token: The token of the user to use in `Authorization` header.
   :>json string password: The password of the user.
   :>json string role:
   :>json string email:
   :>json string _id:
   :>json list databases:
   :>json string defaultDatabase:

.. _Computer:

Computer
--------------------
.. http:get:: (string:database)/devices/computer



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'Computer'}
   :>jsonarr boolean forceCreation: Default: False
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string type: Allowed: {'Desktop', 'Server', 'Microtower', 'Netbook', 'Laptop'}
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/computer/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/computer/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/computer/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/computer/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'Computer'}
   :>json boolean forceCreation: Default: False
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string type: Allowed: {'Desktop', 'Server', 'Microtower', 'Netbook', 'Laptop'}
   :>json float weight: Unit Code: kgm (KGM)
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _ComputerMonitor:

ComputerMonitor
--------------------
.. http:get:: (string:database)/devices/computer-monitor



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string \*serialNumber: 
   :>jsonarr string \*manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string \*model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'ComputerMonitor'}
   :>jsonarr boolean public: Default: False
   :>jsonarr natural inches: 
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string \*type: Allowed: {'TFT', 'LCD', 'LED', 'OLED'}
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/computer-monitor/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/computer-monitor/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/computer-monitor/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/computer-monitor/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string \*serialNumber: 
   :>json string \*manufacturer: 
   :>json string _id: Unique: True
   :>json string \*model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'ComputerMonitor'}
   :>json boolean public: Default: False
   :>json natural inches: 
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*type: Allowed: {'TFT', 'LCD', 'LED', 'OLED'}
   :>json float weight: Unit Code: kgm (KGM)
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _Device:

Device
--------------------
.. http:get:: (string:database)/devices



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr hid hid: 
   :>jsonarr string labelId: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string \*model: 
   :>jsonarr string \*serialNumber: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string \*manufacturer: 
   :>jsonarr string productId: 
   :>jsonarr float memory: Unit Code: mbyte (4L)
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr integer size: Unit Code: mbyte (4L)
   :>jsonarr integer numberOfCores: 
   :>jsonarr list->Component components: Default: []
   :>jsonarr float speed: Unit Code: ghz (A86)
   :>jsonarr string imei: Unique: True
   :>jsonarr boolean public: Default: False
   :>jsonarr string meid: Unique: True
   :>jsonarr natural inches: 
   :>jsonarr dict connectors: 
   :>jsonarr natural connectors.serial: 
   :>jsonarr natural connectors.usb: 
   :>jsonarr natural connectors.pcmcia: 
   :>jsonarr natural connectors.firewire: 
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr list benchmarks: Read only: True
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string \*type: Allowed: {'Router', 'LCD', 'Netbook', 'Printer', 'OLED', 'Switch', 'HUB', 'Terminal', 'Mouse', 'Server', 'Tablet', 'Microtower', 'LED', 'Keyboard', 'Laptop', 'Desktop', 'TFT', 'Smartphone', 'Scanner', 'MultifunctionPrinter', 'SAI'}
   :>jsonarr boolean forceCreation: Default: False
   :>jsonarr string->Device parent: 
   :>jsonarr string \*@type: Allowed: {'NetworkAdapter', 'HardDrive', 'Computer', 'OpticalDrive', 'GraphicCard', 'Mobile', 'Motherboard', 'ComputerMonitor', 'Processor', 'SoundCard', 'Component', 'Peripheral', 'RamModule', 'Device'}
   :>jsonarr dict->devices\:TestHardDrive test: 
   :>jsonarr list tests: Read only: True
   :>jsonarr integer totalSlots: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr list erasures: Read only: True
   :>jsonarr integer usedSlots: 
   :>jsonarr integer maxAcceptedMemory: 
   :>jsonarr string firmwareRevision: 
   :>jsonarr integer sectors: 
   :>jsonarr integer address: Unit Code: bit (A99), Allowed: {256, 128, 64, 32, 8, 16}
   :>jsonarr integer blockSize: 
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/devices/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json hid hid: 
   :>json string labelId: 
   :>json string label: Description: A short, descriptive title
   :>json string \*model: 
   :>json string \*serialNumber: 
   :>json string _id: Unique: True
   :>json string \*manufacturer: 
   :>json string productId: 
   :>json float memory: Unit Code: mbyte (4L)
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json integer size: Unit Code: mbyte (4L)
   :>json integer numberOfCores: 
   :>json list->Component components: Default: []
   :>json float speed: Unit Code: ghz (A86)
   :>json string imei: Unique: True
   :>json boolean public: Default: False
   :>json string meid: Unique: True
   :>json natural inches: 
   :>json dict connectors: 
   :>json natural connectors.serial: 
   :>json natural connectors.usb: 
   :>json natural connectors.pcmcia: 
   :>json natural connectors.firewire: 
   :>json url sameAs: Read only: True, Unique: True
   :>json list benchmarks: Read only: True
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*type: Allowed: {'Router', 'LCD', 'Netbook', 'Printer', 'OLED', 'Switch', 'HUB', 'Terminal', 'Mouse', 'Server', 'Tablet', 'Microtower', 'LED', 'Keyboard', 'Laptop', 'Desktop', 'TFT', 'Smartphone', 'Scanner', 'MultifunctionPrinter', 'SAI'}
   :>json boolean forceCreation: Default: False
   :>json string->Device parent: 
   :>json string \*@type: Allowed: {'NetworkAdapter', 'HardDrive', 'Computer', 'OpticalDrive', 'GraphicCard', 'Mobile', 'Motherboard', 'ComputerMonitor', 'Processor', 'SoundCard', 'Component', 'Peripheral', 'RamModule', 'Device'}
   :>json dict->devices\:TestHardDrive test: 
   :>json list tests: Read only: True
   :>json integer totalSlots: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json list erasures: Read only: True
   :>json integer usedSlots: 
   :>json integer maxAcceptedMemory: 
   :>json string firmwareRevision: 
   :>json integer sectors: 
   :>json integer address: Unit Code: bit (A99), Allowed: {256, 128, 64, 32, 8, 16}
   :>json integer blockSize: 
   :>json float weight: Unit Code: kgm (KGM)
   :>json float height: Unit Code: m (MTR)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:patch:: (string:database)/devices/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string label: Description: A short, descriptive title
   :>json hid hid: 
   :>json string pid: Unique: True
   :>json string \*@type: Allowed: {'NetworkAdapter', 'HardDrive', 'Computer', 'OpticalDrive', 'GraphicCard', 'Mobile', 'Motherboard', 'ComputerMonitor', 'Processor', 'SoundCard', 'Component', 'Peripheral', 'RamModule', 'Device'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string description: Description: Full long description
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Add:

devices:Add
--------------------
.. http:post:: (string:database)/events/devices/add



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Add'}
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json string->Device \*device: 
   :<json list components: Description: Components affected by the event.
   :>json string \*@type: Allowed: {'devices:Add'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/add/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Add'}
   :>json url sameAs: Read only: True, Unique: True
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string->Device \*device: 
   :>json list components: Description: Components affected by the event.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _devices-Allocate:

devices:Allocate
--------------------
.. http:post:: (string:database)/events/devices/allocate



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json email \*to.email: Unique: True
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :>json email \*to.email: Unique: True
   :<json string to.name: Description: The name of an account, if it is a person or an organization.
   :>json string to.name: Description: The name of an account, if it is a person or an organization.
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json objectid->Account_or_dict \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :<json boolean to.isOrganization: 
   :>json objectid->Account_or_dict \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean to.isOrganization: 
   :<json string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json string \*@type: Allowed: {'devices:Allocate'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:Allocate'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/allocate/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json email \*to.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json string to.name: Description: The name of an account, if it is a person or an organization.
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json objectid->Account \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean to.isOrganization: 
   :>json string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string \*@type: Allowed: {'devices:Allocate'}
   :>json url sameAs: Read only: True, Unique: True
   :>json string toOrganization: Doc: Materialization of the organization that, by the time of the allocation, the user worked in., Read only: True, Materialized: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json list components: Description: Components affected by the event., Read only: True
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/allocate/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Deallocate:

devices:Deallocate
--------------------
.. http:post:: (string:database)/events/devices/deallocate



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json objectid->Account from: 
   :>json objectid->Account from: 
   :<json string \*@type: Allowed: {'devices:Deallocate'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:Deallocate'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/deallocate/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json objectid->Account from: 
   :>json string \*@type: Allowed: {'devices:Deallocate'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string fromOrganization: Read only: True
   :>json list components: Description: Components affected by the event., Read only: True
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/deallocate/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-DeviceEvent:

devices:DeviceEvent
--------------------
.. http:get:: (string:database)/events/devices



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string _id:
   :>jsonarr email \*receiver.email: Unique: True
   :>jsonarr email \*to.email: Unique: True
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr dict->Device \*device: 
   :>jsonarr string receiver.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr string to.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>jsonarr objectid->Account \*receiver: Doc: The user that receives it. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>jsonarr boolean receiver.isOrganization: 
   :>jsonarr objectid->Account \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>jsonarr boolean to.isOrganization: 
   :>jsonarr objectid->Account from: 
   :>jsonarr string receiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr dict condition: 
   :>jsonarr list steps: 
   :>jsonarr string byOrganization: Read only: True
   :>jsonarr string fromOrganization: Read only: True
   :>jsonarr integer firstError: 
   :>jsonarr datetime endingTime: 
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string \*type: Allowed: {'CollectionPoint', 'RecyclingPoint', 'FinalUser'}
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string software.productKey: 
   :>jsonarr string snapshotSoftware: Allowed: ['DDI', 'Scan', 'DeviceHubClient'], Default: DDI
   :>jsonarr integer lifetime: 
   :>jsonarr string \*status: 
   :>jsonarr natural \*secureRandomSteps: 
   :>jsonarr string->Device parent: Description: The event triggered in this computer.
   :>jsonarr string \*@type: Allowed: {'devices:Dispose', 'devices:TestHardDrive', 'devices:EventWithOneDevice', 'devices:ToPrepare', 'devices:Remove', 'devices:Register', 'devices:EraseSectors', 'devices:ToRepair', 'devices:Locate', 'devices:ToDispose', 'devices:Add', 'devices:Deallocate', 'devices:Allocate', 'devices:Receive', 'devices:DeviceEvent', 'devices:Repair', 'devices:EraseBasic', 'devices:EventWithDevices', 'devices:Snapshot', 'devices:Ready', 'devices:Free'}
   :>jsonarr boolean \*acceptedConditions: Allowed: {True}
   :>jsonarr string receiverOrganization: Doc: Materialization of the organization that, by the time of the receive, the user worked in., Read only: True, Materialized: True
   :>jsonarr list unsecured: Read only: True, Default: []
   :>jsonarr boolean \*error: 
   :>jsonarr ['boolean'] force: 
   :>jsonarr string toOrganization: Doc: Materialization of the organization that, by the time of the allocation, the user worked in., Read only: True, Materialized: True
   :>jsonarr objectid->Event snapshot: 
   :>jsonarr string request: Read only: True
   :>jsonarr objectid->Place place: Description: Where did it happened
   :>jsonarr boolean offline: 
   :>jsonarr boolean success: 
   :>jsonarr version version: 
   :>jsonarr list \*devices: 
   :>jsonarr boolean automatic: 
   :>jsonarr list events: Read only: True
   :>jsonarr datetime created: 
   :>jsonarr datetime startingTime: 
   :>jsonarr boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>jsonarr list components: Description: Components affected by the event., Read only: True
   :>jsonarr boolean cleanWithZeros: 
   :>jsonarr dict debug: 
   :>jsonarr dict condition.functionality: 
   :>jsonarr string condition.functionality.general: Description: Grades the defects of a device that affect its usage., Allowed: ['A', 'B', 'C', 'D']
   :>jsonarr dict condition.appearance: 
   :>jsonarr string condition.appearance.general: Description: Grades the imperfections that aesthetically affect the device, but not its usage., Allowed: ['A', 'B', 'C', 'D']
   :>jsonarr dict software: 
   :>jsonarr datetime date: Description: When this happened. Leave blank if it is happening now
   :>jsonarr boolean secured: Default: False
   :>jsonarr boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>jsonarr string comment: Description: Short comment for fast and easy reading
   :>jsonarr string description: Description: Full long description
   :>jsonarr point geo: Description: Where did it happened, Excludes: place, OR: ['place']
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json email \*receiver.email: Unique: True
   :>json email \*to.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json dict->Device \*device: 
   :>json string receiver.name: Description: The name of an account, if it is a person or an organization.
   :>json string to.name: Description: The name of an account, if it is a person or an organization.
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json objectid->Account \*receiver: Doc: The user that receives it. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean receiver.isOrganization: 
   :>json objectid->Account \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean to.isOrganization: 
   :>json objectid->Account from: 
   :>json string receiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json dict condition: 
   :>json list steps: 
   :>json string byOrganization: Read only: True
   :>json string fromOrganization: Read only: True
   :>json integer firstError: 
   :>json datetime endingTime: 
   :>json url sameAs: Read only: True, Unique: True
   :>json string \*type: Allowed: {'CollectionPoint', 'RecyclingPoint', 'FinalUser'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string software.productKey: 
   :>json string snapshotSoftware: Allowed: ['DDI', 'Scan', 'DeviceHubClient'], Default: DDI
   :>json integer lifetime: 
   :>json string \*status: 
   :>json natural \*secureRandomSteps: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json string \*@type: Allowed: {'devices:Dispose', 'devices:TestHardDrive', 'devices:EventWithOneDevice', 'devices:ToPrepare', 'devices:Remove', 'devices:Register', 'devices:EraseSectors', 'devices:ToRepair', 'devices:Locate', 'devices:ToDispose', 'devices:Add', 'devices:Deallocate', 'devices:Allocate', 'devices:Receive', 'devices:DeviceEvent', 'devices:Repair', 'devices:EraseBasic', 'devices:EventWithDevices', 'devices:Snapshot', 'devices:Ready', 'devices:Free'}
   :>json boolean \*acceptedConditions: Allowed: {True}
   :>json string receiverOrganization: Doc: Materialization of the organization that, by the time of the receive, the user worked in., Read only: True, Materialized: True
   :>json list unsecured: Read only: True, Default: []
   :>json boolean \*error: 
   :>json ['boolean'] force: 
   :>json string toOrganization: Doc: Materialization of the organization that, by the time of the allocation, the user worked in., Read only: True, Materialized: True
   :>json objectid->Event snapshot: 
   :>json string request: Read only: True
   :>json objectid->Place place: Description: Where did it happened
   :>json boolean offline: 
   :>json boolean success: 
   :>json version version: 
   :>json list \*devices: 
   :>json boolean automatic: 
   :>json list events: Read only: True
   :>json datetime created: 
   :>json datetime startingTime: 
   :>json boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>json list components: Description: Components affected by the event., Read only: True
   :>json boolean cleanWithZeros: 
   :>json dict debug: 
   :>json dict condition.functionality: 
   :>json string condition.functionality.general: Description: Grades the defects of a device that affect its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json dict condition.appearance: 
   :>json string condition.appearance.general: Description: Grades the imperfections that aesthetically affect the device, but not its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json dict software: 
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean secured: Default: False
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Description: Where did it happened, Excludes: place, OR: ['place']
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Dispose:

devices:Dispose
--------------------
.. http:post:: (string:database)/events/devices/dispose



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Dispose'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:Dispose'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/dispose/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Dispose'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/dispose/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-EraseBasic:

devices:EraseBasic
--------------------
.. http:post:: (string:database)/events/devices/erase-basic



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:EraseBasic', 'devices:EraseSectors'}
   :<json string->Device \*device: 
   :<json boolean success: 
   :<json list steps: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime endingTime: 
   :<json datetime startingTime: 
   :<json boolean cleanWithZeros: 
   :<json natural \*secureRandomSteps: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :>json string \*@type: Allowed: {'devices:EraseBasic', 'devices:EraseSectors'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/erase-basic/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:EraseBasic', 'devices:EraseSectors'}
   :>json string->Device \*device: 
   :>json string byOrganization: Read only: True
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean success: 
   :>json list steps: 
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime endingTime: 
   :>json datetime startingTime: 
   :>json boolean cleanWithZeros: 
   :>json natural \*secureRandomSteps: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _devices-EraseSectors:

devices:EraseSectors
--------------------
.. http:post:: (string:database)/events/devices/erase-sectors



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:EraseSectors'}
   :<json string->Device \*device: 
   :<json boolean success: 
   :<json list steps: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime endingTime: 
   :<json datetime startingTime: 
   :<json boolean cleanWithZeros: 
   :<json natural \*secureRandomSteps: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :>json string \*@type: Allowed: {'devices:EraseSectors'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/erase-sectors/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:EraseSectors'}
   :>json string->Device \*device: 
   :>json string byOrganization: Read only: True
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean success: 
   :>json list steps: 
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime endingTime: 
   :>json datetime startingTime: 
   :>json boolean cleanWithZeros: 
   :>json natural \*secureRandomSteps: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _devices-Free:

devices:Free
--------------------
.. http:post:: (string:database)/events/devices/free



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Free'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:Free'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/free/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Free'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/free/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Locate:

devices:Locate
--------------------
.. http:post:: (string:database)/events/devices/locate



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Locate'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json objectid->Place place: Description: Where did it happened
   :>json string \*@type: Allowed: {'devices:Locate'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened, Excludes: place, OR: ['place']
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/locate/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Locate'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json list components: Description: Components affected by the event., Read only: True
   :>json objectid->Place place: Description: Where did it happened
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened, Excludes: place, OR: ['place']
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/locate/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Ready:

devices:Ready
--------------------
.. http:post:: (string:database)/events/devices/ready



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Ready'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:Ready'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/ready/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Ready'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/ready/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Receive:

devices:Receive
--------------------
.. http:post:: (string:database)/events/devices/receive



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json email \*receiver.email: Unique: True
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json string receiver.name: Description: The name of an account, if it is a person or an organization.
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json objectid->Account_or_dict \*receiver: Doc: The user that receives it. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :<json boolean receiver.isOrganization: 
   :<json string receiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json string \*@type: Allowed: {'devices:Receive'}
   :<json boolean \*acceptedConditions: Allowed: {True}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :<json boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :<json objectid->Place place: Description: Where did it happened
   :>json string \*@type: Allowed: {'devices:Receive'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/receive/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json email \*receiver.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json string receiver.name: Description: The name of an account, if it is a person or an organization.
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json objectid->Account \*receiver: Doc: The user that receives it. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean receiver.isOrganization: 
   :>json string receiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string \*@type: Allowed: {'devices:Receive'}
   :>json url sameAs: Read only: True, Unique: True
   :>json string receiverOrganization: Doc: Materialization of the organization that, by the time of the receive, the user worked in., Read only: True, Materialized: True
   :>json boolean \*acceptedConditions: Allowed: {True}
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :>json boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>json list components: Description: Components affected by the event., Read only: True
   :>json objectid->Place place: Description: Where did it happened
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/receive/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Register:

devices:Register
--------------------
.. http:post:: (string:database)/events/devices/register



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Register'}
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json ['boolean'] force: 
   :<json ['dict', 'string']->Device device: 
   :<json ['list', 'string']->Device components: 
   :<json objectid->Place place: Description: Where did it happened
   :>json string \*@type: Allowed: {'devices:Register'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json ['dict', 'string']->Device device: 
   :>json ['list', 'string']->Device components: 
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/register/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Register'}
   :>json url sameAs: Read only: True, Unique: True
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json ['boolean'] force: 
   :>json ['dict', 'string']->Device device: 
   :>json ['list', 'string']->Device components: 
   :>json objectid->Place place: Description: Where did it happened
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/register/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Remove:

devices:Remove
--------------------
.. http:post:: (string:database)/events/devices/remove



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Remove'}
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json string->Device \*device: 
   :<json list components: Description: Components affected by the event.
   :>json string \*@type: Allowed: {'devices:Remove'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/remove/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Remove'}
   :>json url sameAs: Read only: True, Unique: True
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string->Device \*device: 
   :>json list components: Description: Components affected by the event.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _devices-Repair:

devices:Repair
--------------------
.. http:post:: (string:database)/events/devices/repair



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:Repair'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:Repair'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/repair/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:Repair'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/repair/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-Snapshot:

devices:Snapshot
--------------------
.. http:post:: (string:database)/events/devices/snapshot



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json email \*from.email: Unique: True
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json dict->Device \*device: 
   :<json string from.name: Description: The name of an account, if it is a person or an organization.
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json objectid->Account_or_dict from: Description: The e-mail of the person or organization that gave the devices. You cannot change this later., Doc: It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :<json boolean from.isOrganization: 
   :<json string from.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json dict condition: 
   :<json string \*@type: Allowed: {'devices:Snapshot'}
   :<json objectid->Place place: Description: Place the devices to an existing location.
   :<json boolean offline: 
   :<json version version: 
   :<json boolean automatic: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json string software.productKey: 
   :<json string snapshotSoftware: Allowed: ['DDI', 'Scan', 'DeviceHubClient'], Default: DDI
   :<json list components: Default: []
   :<json dict debug: 
   :<json dict condition.functionality: 
   :<json string condition.functionality.general: Description: Grades the defects of a device that affect its usage., Allowed: ['A', 'B', 'C', 'D']
   :<json dict condition.appearance: 
   :<json string condition.appearance.general: Description: Grades the imperfections that aesthetically affect the device, but not its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json string \*@type: Allowed: {'devices:Snapshot'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json dict software: 
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/snapshot/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json email \*from.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json dict->Device \*device: 
   :>json string from.name: Description: The name of an account, if it is a person or an organization.
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json objectid->Account from: Description: The e-mail of the person or organization that gave the devices. You cannot change this later., Doc: It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean from.isOrganization: 
   :>json string from.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json dict condition: 
   :>json string \*@type: Allowed: {'devices:Snapshot'}
   :>json string byOrganization: Read only: True
   :>json list unsecured: Read only: True, Default: []
   :>json string request: Read only: True
   :>json objectid->Place place: Description: Place the devices to an existing location.
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean offline: 
   :>json version version: 
   :>json boolean automatic: 
   :>json list events: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string software.productKey: 
   :>json string snapshotSoftware: Allowed: ['DDI', 'Scan', 'DeviceHubClient'], Default: DDI
   :>json list components: Default: []
   :>json dict debug: 
   :>json dict condition.functionality: 
   :>json string condition.functionality.general: Description: Grades the defects of a device that affect its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json dict condition.appearance: 
   :>json string condition.appearance.general: Description: Grades the imperfections that aesthetically affect the device, but not its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json dict software: 
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/snapshot/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-TestHardDrive:

devices:TestHardDrive
--------------------
.. http:post:: (string:database)/events/devices/test-hard-drive



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:TestHardDrive'}
   :<json string type: 
   :<json boolean \*error: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json objectid->Event snapshot: 
   :<json string->Device \*device: 
   :<json integer firstError: 
   :<json integer lifetime: 
   :<json string \*status: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :>json string \*@type: Allowed: {'devices:TestHardDrive'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/test-hard-drive/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:TestHardDrive'}
   :>json url sameAs: Read only: True, Unique: True
   :>json string type: 
   :>json boolean \*error: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json objectid->Event snapshot: 
   :>json string->Device \*device: 
   :>json integer firstError: 
   :>json integer lifetime: 
   :>json string \*status: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _devices-ToDispose:

devices:ToDispose
--------------------
.. http:post:: (string:database)/events/devices/to-dispose



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:ToDispose'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:ToDispose'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/to-dispose/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:ToDispose'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/to-dispose/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-ToPrepare:

devices:ToPrepare
--------------------
.. http:post:: (string:database)/events/devices/to-prepare



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:ToPrepare'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:ToPrepare'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/to-prepare/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:ToPrepare'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/to-prepare/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _devices-ToRepair:

devices:ToRepair
--------------------
.. http:post:: (string:database)/events/devices/to-repair



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :<json string \*@type: Allowed: {'devices:ToRepair'}
   :<json list \*devices: 
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*@type: Allowed: {'devices:ToRepair'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/devices/to-repair/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string label: Description: A short, descriptive title
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json string \*@type: Allowed: {'devices:ToRepair'}
   :>json url sameAs: Read only: True, Unique: True
   :>json list \*devices: 
   :>json string byOrganization: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string description: Description: Full long description
   :>json string comment: Description: Short comment for fast and easy reading
   :>json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/devices/to-repair/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _Event:

Event
--------------------
.. http:get:: (string:database)/events



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string _id:
   :>jsonarr email \*receiver.email: Unique: True
   :>jsonarr email \*to.email: Unique: True
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr dict->Device \*device: 
   :>jsonarr string receiver.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr string to.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>jsonarr objectid->Account \*receiver: Doc: The user that receives it. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>jsonarr boolean receiver.isOrganization: 
   :>jsonarr objectid->Account \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>jsonarr boolean to.isOrganization: 
   :>jsonarr objectid->Account from: 
   :>jsonarr string receiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr dict condition: 
   :>jsonarr list steps: 
   :>jsonarr string byOrganization: Read only: True
   :>jsonarr string fromOrganization: Read only: True
   :>jsonarr integer firstError: 
   :>jsonarr datetime endingTime: 
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string \*type: Allowed: {'CollectionPoint', 'RecyclingPoint', 'FinalUser'}
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string software.productKey: 
   :>jsonarr string snapshotSoftware: Allowed: ['DDI', 'Scan', 'DeviceHubClient'], Default: DDI
   :>jsonarr integer lifetime: 
   :>jsonarr string \*status: 
   :>jsonarr natural \*secureRandomSteps: 
   :>jsonarr string->Device parent: Description: The event triggered in this computer.
   :>jsonarr string \*@type: Allowed: {'devices:Dispose', 'devices:TestHardDrive', 'devices:EventWithOneDevice', 'devices:ToPrepare', 'devices:Remove', 'devices:Register', 'Event', 'devices:EraseSectors', 'devices:ToRepair', 'devices:Locate', 'devices:ToDispose', 'devices:Add', 'devices:Deallocate', 'devices:Allocate', 'devices:DeviceEvent', 'devices:Receive', 'devices:Repair', 'devices:EraseBasic', 'devices:Snapshot', 'devices:EventWithDevices', 'devices:Ready', 'devices:Free'}
   :>jsonarr boolean \*acceptedConditions: Allowed: {True}
   :>jsonarr string receiverOrganization: Doc: Materialization of the organization that, by the time of the receive, the user worked in., Read only: True, Materialized: True
   :>jsonarr list unsecured: Read only: True, Default: []
   :>jsonarr boolean \*error: 
   :>jsonarr ['boolean'] force: 
   :>jsonarr string toOrganization: Doc: Materialization of the organization that, by the time of the allocation, the user worked in., Read only: True, Materialized: True
   :>jsonarr objectid->Event snapshot: 
   :>jsonarr string request: Read only: True
   :>jsonarr objectid->Place place: Description: Where did it happened
   :>jsonarr boolean offline: 
   :>jsonarr boolean success: 
   :>jsonarr version version: 
   :>jsonarr list \*devices: 
   :>jsonarr boolean automatic: 
   :>jsonarr list events: Read only: True
   :>jsonarr datetime created: 
   :>jsonarr datetime startingTime: 
   :>jsonarr boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>jsonarr list components: Description: Components affected by the event., Read only: True
   :>jsonarr boolean cleanWithZeros: 
   :>jsonarr dict debug: 
   :>jsonarr dict condition.functionality: 
   :>jsonarr string condition.functionality.general: Description: Grades the defects of a device that affect its usage., Allowed: ['A', 'B', 'C', 'D']
   :>jsonarr dict condition.appearance: 
   :>jsonarr string condition.appearance.general: Description: Grades the imperfections that aesthetically affect the device, but not its usage., Allowed: ['A', 'B', 'C', 'D']
   :>jsonarr dict software: 
   :>jsonarr datetime date: Description: When this happened. Leave blank if it is happening now
   :>jsonarr boolean secured: Default: False
   :>jsonarr boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>jsonarr string comment: Description: Short comment for fast and easy reading
   :>jsonarr string description: Description: Full long description
   :>jsonarr point geo: Description: Where did it happened, Excludes: place, OR: ['place']
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/events/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json email \*receiver.email: Unique: True
   :>json email \*to.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json dict->Device \*device: 
   :>json string receiver.name: Description: The name of an account, if it is a person or an organization.
   :>json string to.name: Description: The name of an account, if it is a person or an organization.
   :>json objectid->Account byUser: Roles with writing permission: ('admin', 'superuser')
   :>json objectid->Account \*receiver: Doc: The user that receives it. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean receiver.isOrganization: 
   :>json objectid->Account \*to: Doc: The user the devices are allocated to. It can be a reference to an account, or a basic account object. The object has to contain at least an e-mail. If the e-mail does not match to an existing one, an account is created. If the e-mail exists, that account is used, and the rest of the data (name, org...) is discarded.
   :>json boolean to.isOrganization: 
   :>json objectid->Account from: 
   :>json string receiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string to.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json dict condition: 
   :>json list steps: 
   :>json string byOrganization: Read only: True
   :>json string fromOrganization: Read only: True
   :>json integer firstError: 
   :>json datetime endingTime: 
   :>json url sameAs: Read only: True, Unique: True
   :>json string \*type: Allowed: {'CollectionPoint', 'RecyclingPoint', 'FinalUser'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string software.productKey: 
   :>json string snapshotSoftware: Allowed: ['DDI', 'Scan', 'DeviceHubClient'], Default: DDI
   :>json integer lifetime: 
   :>json string \*status: 
   :>json natural \*secureRandomSteps: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json string \*@type: Allowed: {'devices:Dispose', 'devices:TestHardDrive', 'devices:EventWithOneDevice', 'devices:ToPrepare', 'devices:Remove', 'devices:Register', 'Event', 'devices:EraseSectors', 'devices:ToRepair', 'devices:Locate', 'devices:ToDispose', 'devices:Add', 'devices:Deallocate', 'devices:Allocate', 'devices:DeviceEvent', 'devices:Receive', 'devices:Repair', 'devices:EraseBasic', 'devices:Snapshot', 'devices:EventWithDevices', 'devices:Ready', 'devices:Free'}
   :>json boolean \*acceptedConditions: Allowed: {True}
   :>json string receiverOrganization: Doc: Materialization of the organization that, by the time of the receive, the user worked in., Read only: True, Materialized: True
   :>json list unsecured: Read only: True, Default: []
   :>json boolean \*error: 
   :>json ['boolean'] force: 
   :>json string toOrganization: Doc: Materialization of the organization that, by the time of the allocation, the user worked in., Read only: True, Materialized: True
   :>json objectid->Event snapshot: 
   :>json string request: Read only: True
   :>json objectid->Place place: Description: Where did it happened
   :>json boolean offline: 
   :>json boolean success: 
   :>json version version: 
   :>json list \*devices: 
   :>json boolean automatic: 
   :>json list events: Read only: True
   :>json datetime created: 
   :>json datetime startingTime: 
   :>json boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>json list components: Description: Components affected by the event., Read only: True
   :>json boolean cleanWithZeros: 
   :>json dict debug: 
   :>json dict condition.functionality: 
   :>json string condition.functionality.general: Description: Grades the defects of a device that affect its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json dict condition.appearance: 
   :>json string condition.appearance.general: Description: Grades the imperfections that aesthetically affect the device, but not its usage., Allowed: ['A', 'B', 'C', 'D']
   :>json dict software: 
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean secured: Default: False
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Description: Where did it happened, Excludes: place, OR: ['place']
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/events/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. _GraphicCard:

GraphicCard
--------------------
.. http:get:: (string:database)/devices/graphic-card



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr float memory: Unit Code: mbyte (4L)
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'GraphicCard'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/graphic-card/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/graphic-card/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/graphic-card/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/graphic-card/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json float memory: Unit Code: mbyte (4L)
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'GraphicCard'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _HardDrive:

HardDrive
--------------------
.. http:get:: (string:database)/devices/hard-drive



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr float size: Unit Code: mbyte (4L)
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'HardDrive'}
   :>jsonarr list tests: Read only: True
   :>jsonarr boolean public: Default: False
   :>jsonarr list erasures: Read only: True
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr list benchmarks: Read only: True
   :>jsonarr dict->devices\:TestHardDrive test: 
   :>jsonarr string firmwareRevision: 
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr integer sectors: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr integer blockSize: 
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/hard-drive/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/hard-drive/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/hard-drive/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/hard-drive/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json float size: Unit Code: mbyte (4L)
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'HardDrive'}
   :>json list tests: Read only: True
   :>json boolean public: Default: False
   :>json list erasures: Read only: True
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json list benchmarks: Read only: True
   :>json dict->devices\:TestHardDrive test: 
   :>json string firmwareRevision: 
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json integer sectors: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json integer blockSize: 
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _Mobile:

Mobile
--------------------
.. http:get:: (string:database)/devices/mobile



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string \*serialNumber: 
   :>jsonarr string \*manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string \*model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'Mobile'}
   :>jsonarr string imei: Unique: True
   :>jsonarr boolean public: Default: False
   :>jsonarr string meid: Unique: True
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string \*type: Allowed: {'Smartphone', 'Tablet'}
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/mobile/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/mobile/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/mobile/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/mobile/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string \*serialNumber: 
   :>json string \*manufacturer: 
   :>json string _id: Unique: True
   :>json string \*model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'Mobile'}
   :>json string imei: Unique: True
   :>json boolean public: Default: False
   :>json string meid: Unique: True
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*type: Allowed: {'Smartphone', 'Tablet'}
   :>json float weight: Unit Code: kgm (KGM)
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _Motherboard:

Motherboard
--------------------
.. http:get:: (string:database)/devices/motherboard



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'Motherboard'}
   :>jsonarr integer maxAcceptedMemory: 
   :>jsonarr boolean public: Default: False
   :>jsonarr dict connectors: 
   :>jsonarr natural connectors.serial: 
   :>jsonarr natural connectors.usb: 
   :>jsonarr natural connectors.pcmcia: 
   :>jsonarr natural connectors.firewire: 
   :>jsonarr integer totalSlots: 
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr integer usedSlots: 
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/motherboard/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/motherboard/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/motherboard/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/motherboard/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'Motherboard'}
   :>json integer maxAcceptedMemory: 
   :>json boolean public: Default: False
   :>json dict connectors: 
   :>json natural connectors.serial: 
   :>json natural connectors.usb: 
   :>json natural connectors.pcmcia: 
   :>json natural connectors.firewire: 
   :>json integer totalSlots: 
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json integer usedSlots: 
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _NetworkAdapter:

NetworkAdapter
--------------------
.. http:get:: (string:database)/devices/network-adapter



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr float speed: Unit Code: mbps (E20)
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'NetworkAdapter'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/network-adapter/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/network-adapter/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/network-adapter/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/network-adapter/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json float speed: Unit Code: mbps (E20)
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'NetworkAdapter'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _OpticalDrive:

OpticalDrive
--------------------
.. http:get:: (string:database)/devices/optical-drive



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'OpticalDrive'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/optical-drive/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/optical-drive/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/optical-drive/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/optical-drive/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'OpticalDrive'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _Peripheral:

Peripheral
--------------------
.. http:get:: (string:database)/devices/peripheral



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string \*serialNumber: 
   :>jsonarr string \*manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string \*model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'Peripheral'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string \*type: Allowed: {'Router', 'Keyboard', 'Printer', 'Switch', 'HUB', 'Scanner', 'Terminal', 'SAI', 'MultifunctionPrinter', 'Mouse'}
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/peripheral/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/peripheral/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/peripheral/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/peripheral/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string \*serialNumber: 
   :>json string \*manufacturer: 
   :>json string _id: Unique: True
   :>json string \*model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'Peripheral'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string \*type: Allowed: {'Router', 'Keyboard', 'Printer', 'Switch', 'HUB', 'Scanner', 'Terminal', 'SAI', 'MultifunctionPrinter', 'Mouse'}
   :>json float weight: Unit Code: kgm (KGM)
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _Place:

Place
--------------------
.. http:get:: (string:database)/places



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string _id:
   :>jsonarr string \*label: Description: A short, descriptive title
   :>jsonarr string \*@type: Allowed: {'Place'}
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr objectid->Account byUser: Read only: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr string type: Allowed: {'Zone', 'Warehouse', 'CollectionPoint', 'Department'}
   :>jsonarr string telephone: 
   :>jsonarr list devices: Default: []
   :>jsonarr dict address: 
   :>jsonarr string address.addressRegion: Description: The region. For example, CA.
   :>jsonarr string address.streetAddress: Description: The street address. For example, C/Jordi Girona, 1-3.
   :>jsonarr string address.postalCode: Description: The postal code. For example, 94043.
   :>jsonarr string address.addressCountry: Description: The name of the country, Doc: The addressCountry as per ISO 3166 (2 characters)., Allowed: {'GH', 'SI', 'CZ', 'GL', 'CO', 'NE', 'TK', 'LR', 'LS', 'IO', 'SE', 'CG', 'GN', 'CI', 'PS', 'SS', 'TG', 'MK', 'JO', 'LT', 'ZA', 'AQ', 'IQ', 'SN', 'GA', 'GG', 'MV', 'PE', 'SG', 'KN', 'FK', 'GU', 'BH', 'PG', 'KR', 'CR', 'VI', 'MF', 'PT', 'IE', 'AI', 'LC', 'LB', 'CK', 'TV', 'FO', 'KG', 'MW', 'TT', 'SY', 'GR', 'AD', 'NL', 'MG', 'BV', 'KZ', 'MO', 'GB', 'IS', 'AO', 'RE', 'EC', 'BM', 'NZ', 'BQ', 'CD', 'VU', 'CY', 'KM', 'UM', 'US', 'HR', 'BI', 'OM', 'UZ', 'BT', 'BJ', 'CM', 'SB', 'SV', 'HU', 'BB', 'ID', 'VG', 'ME', 'KH', 'GD', 'AM', 'LI', 'TJ', 'WF', 'ET', 'AZ', 'TO', 'BS', 'MQ', 'TM', 'AS', 'BY', 'AE', 'JM', 'AL', 'TW', 'MR', 'MT', 'MH', 'MN', 'BD', 'RO', 'NF', 'KE', 'MA', 'NG', 'NC', 'LU', 'LY', 'VA', 'UG', 'DO', 'TF', 'BW', 'ZW', 'AT', 'PW', 'CA', 'VN', 'GS', 'UA', 'SX', 'BR', 'IM', 'FI', 'RS', 'SZ', 'HK', 'DZ', 'BF', 'AF', 'DK', 'MY', 'BL', 'NP', 'AR', 'IN', 'MC', 'GI', 'UY', 'KP', 'LV', 'CH', 'FJ', 'ES', 'CV', 'FM', 'GW', 'BN', 'GY', 'HN', 'SH', 'JE', 'NA', 'YE', 'TL', 'NR', 'LK', 'ML', 'SR', 'TN', 'KY', 'BG', 'LA', 'CW', 'MM', 'SL', 'BE', 'RW', 'GE', 'PF', 'ZM', 'EH', 'PH', 'SO', 'TZ', 'MX', 'SM', 'IL', 'WS', 'YT', 'CL', 'NO', 'HT', 'MD', 'TR', 'SA', 'JP', 'VE', 'PY', 'AG', 'SC', 'EE', 'AU', 'NI', 'BZ', 'MS', 'VC', 'PM', 'MU', 'GP', 'SK', 'KW', 'SJ', 'PA', 'HM', 'TH', 'KI', 'PL', 'SD', 'PN', 'CN', 'AX', 'IR', 'GM', 'RU', 'PR', 'QA', 'PK', 'TC', 'GQ', 'AW', 'IT', 'CX', 'DE', 'ER', 'CF', 'DM', 'CC', 'FR', 'TD', 'EG', 'MZ', 'MP', 'ST', 'GT', 'BA', 'NU', 'GF', 'BO', 'CU', 'DJ'}
   :>jsonarr string address.addressLocality: Description: The locality. For example, Barcelona.
   :>jsonarr string description: Description: Full long description
   :>jsonarr polygon geo: Description: Set the area of the place. Be careful! Once set, you cannot update the area., Modifiable: False
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:post:: (string:database)/places



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 201:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>json string _id:
   :<json string \*label: Description: A short, descriptive title
   :>json string \*label: Description: A short, descriptive title
   :<json string \*@type: Allowed: {'Place'}
   :<json datetime created: 
   :<json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :<json string type: Allowed: {'Zone', 'Warehouse', 'CollectionPoint', 'Department'}
   :<json string telephone: 
   :<json list devices: Default: []
   :<json dict address: 
   :<json string address.addressRegion: Description: The region. For example, CA.
   :<json string address.streetAddress: Description: The street address. For example, C/Jordi Girona, 1-3.
   :<json string address.postalCode: Description: The postal code. For example, 94043.
   :<json string address.addressCountry: Description: The name of the country, Doc: The addressCountry as per ISO 3166 (2 characters)., Allowed: {'GH', 'SI', 'CZ', 'GL', 'CO', 'NE', 'TK', 'LR', 'LS', 'IO', 'SE', 'CG', 'GN', 'CI', 'PS', 'SS', 'TG', 'MK', 'JO', 'LT', 'ZA', 'AQ', 'IQ', 'SN', 'GA', 'GG', 'MV', 'PE', 'SG', 'KN', 'FK', 'GU', 'BH', 'PG', 'KR', 'CR', 'VI', 'MF', 'PT', 'IE', 'AI', 'LC', 'LB', 'CK', 'TV', 'FO', 'KG', 'MW', 'TT', 'SY', 'GR', 'AD', 'NL', 'MG', 'BV', 'KZ', 'MO', 'GB', 'IS', 'AO', 'RE', 'EC', 'BM', 'NZ', 'BQ', 'CD', 'VU', 'CY', 'KM', 'UM', 'US', 'HR', 'BI', 'OM', 'UZ', 'BT', 'BJ', 'CM', 'SB', 'SV', 'HU', 'BB', 'ID', 'VG', 'ME', 'KH', 'GD', 'AM', 'LI', 'TJ', 'WF', 'ET', 'AZ', 'TO', 'BS', 'MQ', 'TM', 'AS', 'BY', 'AE', 'JM', 'AL', 'TW', 'MR', 'MT', 'MH', 'MN', 'BD', 'RO', 'NF', 'KE', 'MA', 'NG', 'NC', 'LU', 'LY', 'VA', 'UG', 'DO', 'TF', 'BW', 'ZW', 'AT', 'PW', 'CA', 'VN', 'GS', 'UA', 'SX', 'BR', 'IM', 'FI', 'RS', 'SZ', 'HK', 'DZ', 'BF', 'AF', 'DK', 'MY', 'BL', 'NP', 'AR', 'IN', 'MC', 'GI', 'UY', 'KP', 'LV', 'CH', 'FJ', 'ES', 'CV', 'FM', 'GW', 'BN', 'GY', 'HN', 'SH', 'JE', 'NA', 'YE', 'TL', 'NR', 'LK', 'ML', 'SR', 'TN', 'KY', 'BG', 'LA', 'CW', 'MM', 'SL', 'BE', 'RW', 'GE', 'PF', 'ZM', 'EH', 'PH', 'SO', 'TZ', 'MX', 'SM', 'IL', 'WS', 'YT', 'CL', 'NO', 'HT', 'MD', 'TR', 'SA', 'JP', 'VE', 'PY', 'AG', 'SC', 'EE', 'AU', 'NI', 'BZ', 'MS', 'VC', 'PM', 'MU', 'GP', 'SK', 'KW', 'SJ', 'PA', 'HM', 'TH', 'KI', 'PL', 'SD', 'PN', 'CN', 'AX', 'IR', 'GM', 'RU', 'PR', 'QA', 'PK', 'TC', 'GQ', 'AW', 'IT', 'CX', 'DE', 'ER', 'CF', 'DM', 'CC', 'FR', 'TD', 'EG', 'MZ', 'MP', 'ST', 'GT', 'BA', 'NU', 'GF', 'BO', 'CU', 'DJ'}
   :<json string address.addressLocality: Description: The locality. For example, Barcelona.
   :>json string \*@type: Allowed: {'Place'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json list devices: Default: []
   :<json string description: Description: Full long description
   :>json string description: Description: Full long description
   :<json polygon geo: Description: Set the area of the place. Be careful! Once set, you cannot update the area., Modifiable: False
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:get:: (string:database)/places/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string \*label: Description: A short, descriptive title
   :>json string \*@type: Allowed: {'Place'}
   :>json url sameAs: Read only: True, Unique: True
   :>json objectid->Account byUser: Read only: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string type: Allowed: {'Zone', 'Warehouse', 'CollectionPoint', 'Department'}
   :>json string telephone: 
   :>json list devices: Default: []
   :>json dict address: 
   :>json string address.addressRegion: Description: The region. For example, CA.
   :>json string address.streetAddress: Description: The street address. For example, C/Jordi Girona, 1-3.
   :>json string address.postalCode: Description: The postal code. For example, 94043.
   :>json string address.addressCountry: Description: The name of the country, Doc: The addressCountry as per ISO 3166 (2 characters)., Allowed: {'GH', 'SI', 'CZ', 'GL', 'CO', 'NE', 'TK', 'LR', 'LS', 'IO', 'SE', 'CG', 'GN', 'CI', 'PS', 'SS', 'TG', 'MK', 'JO', 'LT', 'ZA', 'AQ', 'IQ', 'SN', 'GA', 'GG', 'MV', 'PE', 'SG', 'KN', 'FK', 'GU', 'BH', 'PG', 'KR', 'CR', 'VI', 'MF', 'PT', 'IE', 'AI', 'LC', 'LB', 'CK', 'TV', 'FO', 'KG', 'MW', 'TT', 'SY', 'GR', 'AD', 'NL', 'MG', 'BV', 'KZ', 'MO', 'GB', 'IS', 'AO', 'RE', 'EC', 'BM', 'NZ', 'BQ', 'CD', 'VU', 'CY', 'KM', 'UM', 'US', 'HR', 'BI', 'OM', 'UZ', 'BT', 'BJ', 'CM', 'SB', 'SV', 'HU', 'BB', 'ID', 'VG', 'ME', 'KH', 'GD', 'AM', 'LI', 'TJ', 'WF', 'ET', 'AZ', 'TO', 'BS', 'MQ', 'TM', 'AS', 'BY', 'AE', 'JM', 'AL', 'TW', 'MR', 'MT', 'MH', 'MN', 'BD', 'RO', 'NF', 'KE', 'MA', 'NG', 'NC', 'LU', 'LY', 'VA', 'UG', 'DO', 'TF', 'BW', 'ZW', 'AT', 'PW', 'CA', 'VN', 'GS', 'UA', 'SX', 'BR', 'IM', 'FI', 'RS', 'SZ', 'HK', 'DZ', 'BF', 'AF', 'DK', 'MY', 'BL', 'NP', 'AR', 'IN', 'MC', 'GI', 'UY', 'KP', 'LV', 'CH', 'FJ', 'ES', 'CV', 'FM', 'GW', 'BN', 'GY', 'HN', 'SH', 'JE', 'NA', 'YE', 'TL', 'NR', 'LK', 'ML', 'SR', 'TN', 'KY', 'BG', 'LA', 'CW', 'MM', 'SL', 'BE', 'RW', 'GE', 'PF', 'ZM', 'EH', 'PH', 'SO', 'TZ', 'MX', 'SM', 'IL', 'WS', 'YT', 'CL', 'NO', 'HT', 'MD', 'TR', 'SA', 'JP', 'VE', 'PY', 'AG', 'SC', 'EE', 'AU', 'NI', 'BZ', 'MS', 'VC', 'PM', 'MU', 'GP', 'SK', 'KW', 'SJ', 'PA', 'HM', 'TH', 'KI', 'PL', 'SD', 'PN', 'CN', 'AX', 'IR', 'GM', 'RU', 'PR', 'QA', 'PK', 'TC', 'GQ', 'AW', 'IT', 'CX', 'DE', 'ER', 'CF', 'DM', 'CC', 'FR', 'TD', 'EG', 'MZ', 'MP', 'ST', 'GT', 'BA', 'NU', 'GF', 'BO', 'CU', 'DJ'}
   :>json string address.addressLocality: Description: The locality. For example, Barcelona.
   :>json string description: Description: Full long description
   :>json polygon geo: Description: Set the area of the place. Be careful! Once set, you cannot update the area., Modifiable: False
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:patch:: (string:database)/places/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string \*label: Description: A short, descriptive title
   :>json string \*@type: Allowed: {'Place'}
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json list devices: Default: []
   :>json string description: Description: Full long description
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/places/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:put:: (string:database)/places/(regex("[a-f0-9]{24}"):_id)



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string _id:
   :>json string \*label: Description: A short, descriptive title
   :>json string \*@type: Allowed: {'Place'}
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json string type: Allowed: {'Zone', 'Warehouse', 'CollectionPoint', 'Department'}
   :>json string telephone: 
   :>json list devices: Default: []
   :>json dict address: 
   :>json string address.addressRegion: Description: The region. For example, CA.
   :>json string address.streetAddress: Description: The street address. For example, C/Jordi Girona, 1-3.
   :>json string address.postalCode: Description: The postal code. For example, 94043.
   :>json string address.addressCountry: Description: The name of the country, Doc: The addressCountry as per ISO 3166 (2 characters)., Allowed: {'GH', 'SI', 'CZ', 'GL', 'CO', 'NE', 'TK', 'LR', 'LS', 'IO', 'SE', 'CG', 'GN', 'CI', 'PS', 'SS', 'TG', 'MK', 'JO', 'LT', 'ZA', 'AQ', 'IQ', 'SN', 'GA', 'GG', 'MV', 'PE', 'SG', 'KN', 'FK', 'GU', 'BH', 'PG', 'KR', 'CR', 'VI', 'MF', 'PT', 'IE', 'AI', 'LC', 'LB', 'CK', 'TV', 'FO', 'KG', 'MW', 'TT', 'SY', 'GR', 'AD', 'NL', 'MG', 'BV', 'KZ', 'MO', 'GB', 'IS', 'AO', 'RE', 'EC', 'BM', 'NZ', 'BQ', 'CD', 'VU', 'CY', 'KM', 'UM', 'US', 'HR', 'BI', 'OM', 'UZ', 'BT', 'BJ', 'CM', 'SB', 'SV', 'HU', 'BB', 'ID', 'VG', 'ME', 'KH', 'GD', 'AM', 'LI', 'TJ', 'WF', 'ET', 'AZ', 'TO', 'BS', 'MQ', 'TM', 'AS', 'BY', 'AE', 'JM', 'AL', 'TW', 'MR', 'MT', 'MH', 'MN', 'BD', 'RO', 'NF', 'KE', 'MA', 'NG', 'NC', 'LU', 'LY', 'VA', 'UG', 'DO', 'TF', 'BW', 'ZW', 'AT', 'PW', 'CA', 'VN', 'GS', 'UA', 'SX', 'BR', 'IM', 'FI', 'RS', 'SZ', 'HK', 'DZ', 'BF', 'AF', 'DK', 'MY', 'BL', 'NP', 'AR', 'IN', 'MC', 'GI', 'UY', 'KP', 'LV', 'CH', 'FJ', 'ES', 'CV', 'FM', 'GW', 'BN', 'GY', 'HN', 'SH', 'JE', 'NA', 'YE', 'TL', 'NR', 'LK', 'ML', 'SR', 'TN', 'KY', 'BG', 'LA', 'CW', 'MM', 'SL', 'BE', 'RW', 'GE', 'PF', 'ZM', 'EH', 'PH', 'SO', 'TZ', 'MX', 'SM', 'IL', 'WS', 'YT', 'CL', 'NO', 'HT', 'MD', 'TR', 'SA', 'JP', 'VE', 'PY', 'AG', 'SC', 'EE', 'AU', 'NI', 'BZ', 'MS', 'VC', 'PM', 'MU', 'GP', 'SK', 'KW', 'SJ', 'PA', 'HM', 'TH', 'KI', 'PL', 'SD', 'PN', 'CN', 'AX', 'IR', 'GM', 'RU', 'PR', 'QA', 'PK', 'TC', 'GQ', 'AW', 'IT', 'CX', 'DE', 'ER', 'CF', 'DM', 'CC', 'FR', 'TD', 'EG', 'MZ', 'MP', 'ST', 'GT', 'BA', 'NU', 'GF', 'BO', 'CU', 'DJ'}
   :>json string address.addressLocality: Description: The locality. For example, Barcelona.
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _Processor:

Processor
--------------------
.. http:get:: (string:database)/devices/processor



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr float speed: Unit Code: ghz (A86)
   :>jsonarr list components: Default: []
   :>jsonarr integer numberOfCores: 
   :>jsonarr string \*@type: Allowed: {'Processor'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr list benchmarks: Read only: True
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr integer address: Unit Code: bit (A99), Allowed: {256, 128, 64, 32, 8, 16}
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/processor/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/processor/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/processor/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/processor/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json float speed: Unit Code: ghz (A86)
   :>json list components: Default: []
   :>json integer numberOfCores: 
   :>json string \*@type: Allowed: {'Processor'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json list benchmarks: Read only: True
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json integer address: Unit Code: bit (A99), Allowed: {256, 128, 64, 32, 8, 16}
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _RamModule:

RamModule
--------------------
.. http:get:: (string:database)/devices/ram-module



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr integer size: Unit Code: mbyte (4L)
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'RamModule'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr float speed: Unit Code: mhz (MHZ)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/ram-module/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/ram-module/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/ram-module/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/ram-module/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json integer size: Unit Code: mbyte (4L)
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'RamModule'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json float weight: Unit Code: kgm (KGM)
   :>json float speed: Unit Code: mhz (MHZ)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. _SoundCard:

SoundCard
--------------------
.. http:get:: (string:database)/devices/sound-card



   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=1, must-revalidate
   :>jsonarr string pid: Unique: True
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string productId: 
   :>jsonarr objectid->Place place: Materialized: True
   :>jsonarr list owners: Materialized: True
   :>jsonarr list components: Default: []
   :>jsonarr string \*@type: Allowed: {'SoundCard'}
   :>jsonarr boolean public: Default: False
   :>jsonarr url sameAs: Read only: True, Unique: True
   :>jsonarr string->Device parent: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list events: Materialized: True
   :>jsonarr datetime created: 
   :>jsonarr url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr string interface: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr datetime _updated:
   :>jsonarr datetime _created:
   :>json list _items: Contains the actual data, *Response JSON Array of Objects*.
   :>json dict _meta: Provides pagination data.
   :>json natural _meta.max_results: Maximum number of elements in `_items`.
   :>json natural _meta.total: Total of elements.
   :>json natural _meta.page: Actual page number.
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself* and to the *parent*. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/devices/sound-card/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/sound-card/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 204:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
 

.. http:get:: (string:database)/devices/sound-card/(regex("[\w]+"):_id)



    Additional Lookup: (string:database)/devices/sound-card/*(regex("[\w]+-[\w]+-[\w]+"):hid)*

   :reqheader Accept: "application/json"
   :resheader Content-Type: "application/json"
   :resheader Date: The server date
   :resheader Content-Length:
   :resheader Server:
   :statuscode 400:
   :statuscode 422: Document fails validation.
   :statuscode 403:
   :statuscode 404:
   :statuscode 405:
   :statuscode 406:
   :statuscode 415:
   :statuscode 500: Any non-documented error. Please, report if you get this code.
   :reqheader Authorization: "Basic" + space + token from *POST /login*
   :statuscode 200:
   :resheader Cache-Control: max-age=120, must-revalidate
   :resheader Last-Modified: The date when the resource was modified
   :resheader Link: The link at the context, as in http://www.w3.org/ns/json-ld#context
   :>json string pid: Unique: True
   :>json string labelId: 
   :>json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string productId: 
   :>json objectid->Place place: Materialized: True
   :>json list owners: Materialized: True
   :>json list components: Default: []
   :>json string \*@type: Allowed: {'SoundCard'}
   :>json boolean public: Default: False
   :>json url sameAs: Read only: True, Unique: True
   :>json string->Device parent: 
   :>json boolean isUidSecured: Default: True
   :>json list events: Materialized: True
   :>json datetime created: 
   :>json url url: Doc: The url of the resource. If passed in, the value it is moved to sameAs.
   :>json float weight: Unit Code: kgm (KGM)
   :>json string interface: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

