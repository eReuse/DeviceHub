API Endpoints
=============
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
   :>jsonarr list fingerprints: Read only: True
   :>jsonarr string role: Allowed: {'basic', 'employee', 'superuser', 'amateur', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :>jsonarr string \*@type: Allowed: {'Account'}
   :>jsonarr boolean active: Default: True, Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>jsonarr boolean blocked: Default: True, Description: As a manager, you need to specifically accept the user by unblocking it's account., Roles with writing permission: ('admin', 'superuser')
   :>jsonarr list \*databases: Roles with writing permission: ('admin', 'superuser')
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
   :<json string organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json string publicKey: Write only: True
   :<json string role: Allowed: {'basic', 'employee', 'superuser', 'amateur', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :<json string \*@type: Allowed: {'Account'}
   :>json string \*@type: Allowed: {'Account'}
   :>json string role: Allowed: {'basic', 'employee', 'superuser', 'amateur', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :<json boolean active: Default: True, Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>json boolean active: Default: True, Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :<json boolean blocked: Default: True, Description: As a manager, you need to specifically accept the user by unblocking it's account., Roles with writing permission: ('admin', 'superuser')
   :<json list \*databases: Roles with writing permission: ('admin', 'superuser')
   :>json list \*databases: Roles with writing permission: ('admin', 'superuser')
   :<json string defaultDatabase: Roles with writing permission: ('admin', 'superuser')
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:patch:: (string:database)/accounts/(regex("[a-f0-9]{24}"):_id)



    Additional Lookup: (string:database)/accounts/*(regex("[\w]+"):email)*

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
   :>json string \*@type: Allowed: {'Account'}
   :>json string role: Allowed: {'basic', 'employee', 'superuser', 'amateur', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :>json boolean active: Default: True, Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>json list \*databases: Roles with writing permission: ('admin', 'superuser')
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

.. http:delete:: (string:database)/accounts/(regex("[a-f0-9]{24}"):_id)



    Additional Lookup: (string:database)/accounts/*(regex("[\w]+"):email)*

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



    Additional Lookup: (string:database)/accounts/*(regex("[\w]+"):email)*

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
   :>json list fingerprints: Read only: True
   :>json string role: Allowed: {'basic', 'employee', 'superuser', 'amateur', 'admin'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :>json string \*@type: Allowed: {'Account'}
   :>json boolean active: Default: True, Description: Activate the account so you can start using it., Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>json boolean blocked: Default: True, Description: As a manager, you need to specifically accept the user by unblocking it's account., Roles with writing permission: ('admin', 'superuser')
   :>json list \*databases: Roles with writing permission: ('admin', 'superuser')
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

Add
--------------------
.. http:post:: (string:database)/events/add



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
   :<json url sameAs: 
   :<json list->Device components: Description: Components affected by the event.
   :<json string->Device \*device: 
   :<json string \*@type: Allowed: {'Add'}
   :>json string \*@type: Allowed: {'Add'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Allocate
--------------------
.. http:post:: (string:database)/events/allocate



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
   :<json email \*unregisteredTo.email: Unique: True
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json string unregisteredTo.name: Description: The name of an account, if it is a person or an organization.
   :<json dict unregisteredTo: 
   :<json boolean unregisteredTo.isOrganization: 
   :<json objectid->Account to: Excludes: unregisteredTo, OR: ['unregisteredTo']
   :<json string unregisteredTo.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json boolean undefinedDate: Default: False, Excludes: date, Description: Check this to say: "This owner possessed the device for an undetermined amount of time".
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Allocate'}
   :>json string \*@type: Allowed: {'Allocate'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Deallocate
--------------------
.. http:post:: (string:database)/events/deallocate



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
   :<json objectid->Account from: 
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Deallocate'}
   :>json string \*@type: Allowed: {'Deallocate'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

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
   :>jsonarr hid hid: 
   :>jsonarr string pid: Unique: True
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string labelId: 
   :>jsonarr string manufacturer: 
   :>jsonarr string model: 
   :>jsonarr string serialNumber: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string productId: 
   :>jsonarr float memory: Unit Code: mbyte (4L)
   :>jsonarr objectid->Place place: Read only: True
   :>jsonarr list->Account owners: Read only: True
   :>jsonarr integer size: Unit Code: mbyte (4L)
   :>jsonarr float speed: Unit Code: ghz (A86)
   :>jsonarr integer numberOfCores: 
   :>jsonarr list->Device components: Default: []
   :>jsonarr url sameAs: 
   :>jsonarr dict_of_TestHardDrive test: 
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr string type: Allowed: {'Terminal', 'Scanner', 'MultifunctionPrinter', 'Netbook', 'LCD', 'SAI', 'Keyboard', 'Switch', 'TFT', 'Laptop', 'HUB', 'Microtower', 'Server', 'Router', 'Mouse', 'Printer', 'Desktop'}
   :>jsonarr integer maxAcceptedMemory: 
   :>jsonarr url url: Read only: True
   :>jsonarr string->Device parent: 
   :>jsonarr string \*@type: Allowed: {'GraphicCard', 'Peripheral', 'HardDrive', 'Device', 'NetworkAdapter', 'SoundCard', 'Mobile', 'OpticalDrive', 'Processor', 'Computer', 'MobilePhone', 'RamModule', 'Component', 'Motherboard', 'TabletComputer', 'ComputerMonitor'}
   :>jsonarr integer usedSlots: 
   :>jsonarr boolean forceCreation: Default: False
   :>jsonarr integer totalSlots: 
   :>jsonarr string imei: Unique: True
   :>jsonarr list_of_BenchmarkProcessor benchmarks: Read only: True
   :>jsonarr list->Event erasures: Read only: True
   :>jsonarr dict connectors: 
   :>jsonarr natural connectors.firewire: 
   :>jsonarr natural connectors.serial: 
   :>jsonarr natural connectors.pcmcia: 
   :>jsonarr natural connectors.usb: 
   :>jsonarr string meid: Unique: True
   :>jsonarr boolean public: Default: False
   :>jsonarr list->Event tests: Read only: True
   :>jsonarr natural inches: 
   :>jsonarr integer blockSize: 
   :>jsonarr string firmwareRevision: 
   :>jsonarr string interface: 
   :>jsonarr integer sectors: 
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr integer address: Allowed: {256, 32, 64, 128, 8, 16}, Unit Code: bit (A99)
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr string description: Description: Full long description
   :>jsonarr string icon: Read only: True
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
   :>json hid hid: 
   :>json string pid: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json string labelId: 
   :>json string manufacturer: 
   :>json string model: 
   :>json string serialNumber: 
   :>json string _id: Unique: True
   :>json string productId: 
   :>json float memory: Unit Code: mbyte (4L)
   :>json objectid->Place place: Read only: True
   :>json list->Account owners: Read only: True
   :>json integer size: Unit Code: mbyte (4L)
   :>json float speed: Unit Code: ghz (A86)
   :>json integer numberOfCores: 
   :>json list->Device components: Default: []
   :>json url sameAs: 
   :>json dict_of_TestHardDrive test: 
   :>json boolean isUidSecured: Default: True
   :>json string type: Allowed: {'Terminal', 'Scanner', 'MultifunctionPrinter', 'Netbook', 'LCD', 'SAI', 'Keyboard', 'Switch', 'TFT', 'Laptop', 'HUB', 'Microtower', 'Server', 'Router', 'Mouse', 'Printer', 'Desktop'}
   :>json integer maxAcceptedMemory: 
   :>json url url: Read only: True
   :>json string->Device parent: 
   :>json string \*@type: Allowed: {'GraphicCard', 'Peripheral', 'HardDrive', 'Device', 'NetworkAdapter', 'SoundCard', 'Mobile', 'OpticalDrive', 'Processor', 'Computer', 'MobilePhone', 'RamModule', 'Component', 'Motherboard', 'TabletComputer', 'ComputerMonitor'}
   :>json integer usedSlots: 
   :>json boolean forceCreation: Default: False
   :>json integer totalSlots: 
   :>json string imei: Unique: True
   :>json list_of_BenchmarkProcessor benchmarks: Read only: True
   :>json list->Event erasures: Read only: True
   :>json dict connectors: 
   :>json natural connectors.firewire: 
   :>json natural connectors.serial: 
   :>json natural connectors.pcmcia: 
   :>json natural connectors.usb: 
   :>json string meid: Unique: True
   :>json boolean public: Default: False
   :>json list->Event tests: Read only: True
   :>json natural inches: 
   :>json integer blockSize: 
   :>json string firmwareRevision: 
   :>json string interface: 
   :>json integer sectors: 
   :>json float height: Unit Code: m (MTR)
   :>json float weight: Unit Code: kgm (KGM)
   :>json integer address: Allowed: {256, 32, 64, 128, 8, 16}, Unit Code: bit (A99)
   :>json float width: Unit Code: m (MTR)
   :>json string description: Description: Full long description
   :>json string icon: Read only: True
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
   :>json string \*@type: Allowed: {'GraphicCard', 'Peripheral', 'HardDrive', 'Device', 'NetworkAdapter', 'SoundCard', 'Mobile', 'OpticalDrive', 'Processor', 'Computer', 'MobilePhone', 'RamModule', 'Component', 'Motherboard', 'TabletComputer', 'ComputerMonitor'}
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Dispose
--------------------
.. http:post:: (string:database)/events/dispose



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Dispose'}
   :>json string \*@type: Allowed: {'Dispose'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

EraseBasic
--------------------
.. http:post:: (string:database)/events/erase-basic



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
   :<json datetime startingTime: 
   :<json boolean cleanWithZeros: 
   :<json natural \*secureRandomSteps: 
   :<json boolean success: 
   :<json list steps: 
   :<json datetime steps.startingTime: 
   :<json boolean steps.cleanWithZeros: 
   :<json boolean steps.secureRandomSteps: 
   :<json boolean \*steps.success: 
   :<json datetime steps.endingTime: 
   :<json string \*steps.@type: Allowed: {'Zeros', 'Random'}
   :<json datetime endingTime: 
   :<json url sameAs: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :<json string->Device \*device: 
   :<json string \*@type: Allowed: {'EraseSectors', 'EraseBasic'}
   :>json string \*@type: Allowed: {'EraseSectors', 'EraseBasic'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

EraseSectors
--------------------
.. http:post:: (string:database)/events/erase-sectors



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
   :<json datetime startingTime: 
   :<json boolean cleanWithZeros: 
   :<json natural \*secureRandomSteps: 
   :<json boolean success: 
   :<json list steps: 
   :<json datetime steps.startingTime: 
   :<json boolean steps.cleanWithZeros: 
   :<json boolean steps.secureRandomSteps: 
   :<json boolean \*steps.success: 
   :<json datetime steps.endingTime: 
   :<json string \*steps.@type: Allowed: {'Zeros', 'Random'}
   :<json datetime endingTime: 
   :<json url sameAs: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :<json string->Device \*device: 
   :<json string \*@type: Allowed: {'EraseSectors'}
   :>json string \*@type: Allowed: {'EraseSectors'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

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
   :>jsonarr email \*unregisteredReceiver.email: Unique: True
   :>jsonarr email \*unregisteredTo.email: Unique: True
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string unregisteredReceiver.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr string unregisteredTo.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr objectid->Account to: Excludes: unregisteredTo, OR: ['unregisteredTo']
   :>jsonarr dict unregisteredReceiver: 
   :>jsonarr boolean unregisteredReceiver.isOrganization: 
   :>jsonarr objectid->Account from: 
   :>jsonarr objectid->Account byUser: Read only: True
   :>jsonarr objectid->Account receiver: Excludes: unregisteredReceiver, OR: ['unregisteredReceiver']
   :>jsonarr dict unregisteredTo: 
   :>jsonarr boolean unregisteredTo.isOrganization: 
   :>jsonarr string unregisteredReceiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr string unregisteredTo.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr boolean \*acceptedConditions: Allowed: {True}
   :>jsonarr string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :>jsonarr string fromOrganization: Read only: True
   :>jsonarr url sameAs: 
   :>jsonarr ['boolean'] force: 
   :>jsonarr boolean automaticallyAllocate: Default: False, Description: Allocates to the user
   :>jsonarr version version: 
   :>jsonarr string request: Read only: True
   :>jsonarr boolean cleanWithZeros: 
   :>jsonarr string \*status: 
   :>jsonarr boolean success: 
   :>jsonarr boolean undefinedDate: Default: False, Excludes: date, Description: Check this to say: "This owner possessed the device for an undetermined amount of time".
   :>jsonarr string byOrganization: Read only: True
   :>jsonarr boolean \*error: 
   :>jsonarr objectid->Event snapshot: 
   :>jsonarr boolean automatic: 
   :>jsonarr url url: Read only: True
   :>jsonarr string \*@type: Allowed: {'ToRepair', 'Event', 'EventWithOneDevice', 'EraseSectors', 'Receive', 'ToPrepare', 'Free', 'Repair', 'TestHardDrive', 'Ready', 'Locate', 'ToDispose', 'Add', 'Register', 'Snapshot', 'Allocate', 'Remove', 'EraseBasic', 'Dispose', 'EventWithDevices', 'Deallocate'}
   :>jsonarr integer lifetime: 
   :>jsonarr datetime startingTime: 
   :>jsonarr datetime endingTime: 
   :>jsonarr list->Device \*devices: 
   :>jsonarr objectid->Place place: Description: Where did it happened
   :>jsonarr natural \*secureRandomSteps: 
   :>jsonarr integer firstError: 
   :>jsonarr list unsecured: Default: [], Read only: True
   :>jsonarr string->Device unsecured._id: 
   :>jsonarr string unsecured.type: Allowed: {'model', 'pid'}
   :>jsonarr string unsecured.@type: 
   :>jsonarr list->Event events: Read only: True
   :>jsonarr list->Device components: Description: Components affected by the event., Read only: True
   :>jsonarr string toOrganization: Read only: True
   :>jsonarr boolean offline: 
   :>jsonarr string->Device parent: Description: The event triggered in this computer.
   :>jsonarr dict debug: 
   :>jsonarr string receiverOrganization: Read only: True
   :>jsonarr dict->Device \*device: 
   :>jsonarr list steps: 
   :>jsonarr datetime steps.startingTime: 
   :>jsonarr boolean steps.cleanWithZeros: 
   :>jsonarr boolean steps.secureRandomSteps: 
   :>jsonarr boolean \*steps.success: 
   :>jsonarr datetime steps.endingTime: 
   :>jsonarr string \*steps.@type: Allowed: {'Zeros', 'Random'}
   :>jsonarr datetime date: Description: When this happened. Leave blank if it is happening now
   :>jsonarr boolean secured: Default: False
   :>jsonarr boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :>jsonarr string comment: Description: Short comment for fast and easy reading
   :>jsonarr string description: Description: Full long description
   :>jsonarr point geo: Excludes: place, Description: Where did it happened, OR: ['place']
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
   :>json email \*unregisteredReceiver.email: Unique: True
   :>json email \*unregisteredTo.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json string unregisteredReceiver.name: Description: The name of an account, if it is a person or an organization.
   :>json string unregisteredTo.name: Description: The name of an account, if it is a person or an organization.
   :>json objectid->Account to: Excludes: unregisteredTo, OR: ['unregisteredTo']
   :>json dict unregisteredReceiver: 
   :>json boolean unregisteredReceiver.isOrganization: 
   :>json objectid->Account from: 
   :>json objectid->Account byUser: Read only: True
   :>json objectid->Account receiver: Excludes: unregisteredReceiver, OR: ['unregisteredReceiver']
   :>json dict unregisteredTo: 
   :>json boolean unregisteredTo.isOrganization: 
   :>json string unregisteredReceiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string unregisteredTo.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json boolean \*acceptedConditions: Allowed: {True}
   :>json string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :>json string fromOrganization: Read only: True
   :>json url sameAs: 
   :>json ['boolean'] force: 
   :>json boolean automaticallyAllocate: Default: False, Description: Allocates to the user
   :>json version version: 
   :>json string request: Read only: True
   :>json boolean cleanWithZeros: 
   :>json string \*status: 
   :>json boolean success: 
   :>json boolean undefinedDate: Default: False, Excludes: date, Description: Check this to say: "This owner possessed the device for an undetermined amount of time".
   :>json string byOrganization: Read only: True
   :>json boolean \*error: 
   :>json objectid->Event snapshot: 
   :>json boolean automatic: 
   :>json url url: Read only: True
   :>json string \*@type: Allowed: {'ToRepair', 'Event', 'EventWithOneDevice', 'EraseSectors', 'Receive', 'ToPrepare', 'Free', 'Repair', 'TestHardDrive', 'Ready', 'Locate', 'ToDispose', 'Add', 'Register', 'Snapshot', 'Allocate', 'Remove', 'EraseBasic', 'Dispose', 'EventWithDevices', 'Deallocate'}
   :>json integer lifetime: 
   :>json datetime startingTime: 
   :>json datetime endingTime: 
   :>json list->Device \*devices: 
   :>json objectid->Place place: Description: Where did it happened
   :>json natural \*secureRandomSteps: 
   :>json integer firstError: 
   :>json list unsecured: Default: [], Read only: True
   :>json string->Device unsecured._id: 
   :>json string unsecured.type: Allowed: {'model', 'pid'}
   :>json string unsecured.@type: 
   :>json list->Event events: Read only: True
   :>json list->Device components: Description: Components affected by the event., Read only: True
   :>json string toOrganization: Read only: True
   :>json boolean offline: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json dict debug: 
   :>json string receiverOrganization: Read only: True
   :>json dict->Device \*device: 
   :>json list steps: 
   :>json datetime steps.startingTime: 
   :>json boolean steps.cleanWithZeros: 
   :>json boolean steps.secureRandomSteps: 
   :>json boolean \*steps.success: 
   :>json datetime steps.endingTime: 
   :>json string \*steps.@type: Allowed: {'Zeros', 'Random'}
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean secured: Default: False
   :>json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Excludes: place, Description: Where did it happened, OR: ['place']
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Free
--------------------
.. http:post:: (string:database)/events/free



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Free'}
   :>json string \*@type: Allowed: {'Free'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Locate
--------------------
.. http:post:: (string:database)/events/locate



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json objectid->Place place: Description: Where did it happened
   :<json string \*@type: Allowed: {'Locate'}
   :>json string \*@type: Allowed: {'Locate'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Excludes: place, Description: Where did it happened, OR: ['place']
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

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
   :>jsonarr string type: Allowed: {'CollectionPoint', 'Warehouse', 'Zone', 'Department'}
   :>jsonarr list->Device devices: Default: []
   :>jsonarr url sameAs: 
   :>jsonarr objectid->Account byUser: Read only: True
   :>jsonarr url url: Read only: True
   :>jsonarr string \*@type: Allowed: {'Place'}
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
   :<json string type: Allowed: {'CollectionPoint', 'Warehouse', 'Zone', 'Department'}
   :<json list->Device devices: Default: []
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Place'}
   :>json string \*@type: Allowed: {'Place'}
   :>json list->Device devices: Default: []
   :<json string description: Description: Full long description
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
   :>json string type: Allowed: {'CollectionPoint', 'Warehouse', 'Zone', 'Department'}
   :>json list->Device devices: Default: []
   :>json url sameAs: 
   :>json objectid->Account byUser: Read only: True
   :>json url url: Read only: True
   :>json string \*@type: Allowed: {'Place'}
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
   :>json list->Device devices: Default: []
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
   :>json string type: Allowed: {'CollectionPoint', 'Warehouse', 'Zone', 'Department'}
   :>json list->Device devices: Default: []
   :>json url sameAs: 
   :>json string \*@type: Allowed: {'Place'}
   :>json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Ready
--------------------
.. http:post:: (string:database)/events/ready



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Ready'}
   :>json string \*@type: Allowed: {'Ready'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Receive
--------------------
.. http:post:: (string:database)/events/receive



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
   :<json email \*unregisteredReceiver.email: Unique: True
   :<json string label: Description: A short, descriptive title
   :>json string label: Description: A short, descriptive title
   :<json string unregisteredReceiver.name: Description: The name of an account, if it is a person or an organization.
   :<json dict unregisteredReceiver: 
   :<json boolean unregisteredReceiver.isOrganization: 
   :<json objectid->Account receiver: Excludes: unregisteredReceiver, OR: ['unregisteredReceiver']
   :<json string unregisteredReceiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json boolean \*acceptedConditions: Allowed: {True}
   :<json string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json objectid->Place place: Description: Where did it happened
   :<json boolean automaticallyAllocate: Default: False, Description: Allocates to the user
   :<json string \*@type: Allowed: {'Receive'}
   :>json string \*@type: Allowed: {'Receive'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Register
--------------------
.. http:post:: (string:database)/events/register



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
   :<json list_of_Component->Device components: 
   :<json url sameAs: 
   :<json objectid->Place place: Description: Where did it happened
   :<json ['boolean'] force: 
   :<json dict_of_Device->Device device: 
   :<json string \*@type: Allowed: {'Register'}
   :>json string \*@type: Allowed: {'Register'}
   :>json dict_of_Device->Device device: 
   :>json list_of_Component->Device components: 
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Remove
--------------------
.. http:post:: (string:database)/events/remove



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
   :<json url sameAs: 
   :<json list->Device components: Description: Components affected by the event.
   :<json string->Device \*device: 
   :<json string \*@type: Allowed: {'Remove'}
   :>json string \*@type: Allowed: {'Remove'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

Repair
--------------------
.. http:post:: (string:database)/events/repair



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'Repair'}
   :>json string \*@type: Allowed: {'Repair'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 
.. _snapshot:

Snapshot
--------------------
.. http:post:: (string:database)/events/snapshot



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
   :<json url sameAs: 
   :<json version version: 
   :<json list_of_Component->Device components: Default: []
   :<json dict_of_Device->Device \*device: 
   :<json boolean offline: 
   :<json boolean automatic: 
   :<json objectid->Place place: Description: Where did it happened
   :<json dict debug: 
   :<json string \*@type: Allowed: {'Snapshot'}
   :>json string \*@type: Allowed: {'Snapshot'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

TestHardDrive
--------------------
.. http:post:: (string:database)/events/test-hard-drive



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
   :<json integer lifetime: 
   :<json string \*status: 
   :<json string type: 
   :<json url sameAs: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :<json string->Device \*device: 
   :<json objectid->Event snapshot: 
   :<json integer firstError: 
   :<json boolean \*error: 
   :<json string \*@type: Allowed: {'TestHardDrive'}
   :>json string \*@type: Allowed: {'TestHardDrive'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

ToDispose
--------------------
.. http:post:: (string:database)/events/to-dispose



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'ToDispose'}
   :>json string \*@type: Allowed: {'ToDispose'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

ToPrepare
--------------------
.. http:post:: (string:database)/events/to-prepare



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'ToPrepare'}
   :>json string \*@type: Allowed: {'ToPrepare'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

ToRepair
--------------------
.. http:post:: (string:database)/events/to-repair



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
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :<json string \*@type: Allowed: {'ToRepair'}
   :>json string \*@type: Allowed: {'ToRepair'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Default: False, Description: Check if something went wrong, you can add details in a comment
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

