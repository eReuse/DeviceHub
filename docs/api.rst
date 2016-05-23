API
===
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
   :>jsonarr list fingerprints: Read only: True
   :>jsonarr string role: Allowed: {'basic', 'superuser', 'admin', 'employee', 'amateur'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :>jsonarr boolean active: Description: Activate the account so you can start using it., Default: True, Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>jsonarr boolean blocked: Description: As a manager, you need to specifically accept the user by unblocking it's account., Default: True, Roles with writing permission: ('admin', 'superuser')
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
   :<json string \*@type: Allowed: {'Account'}
   :<json string role: Allowed: {'basic', 'superuser', 'admin', 'employee', 'amateur'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :<json string publicKey: Write only: True
   :>json string \*@type: Allowed: {'Account'}
   :>json string role: Allowed: {'basic', 'superuser', 'admin', 'employee', 'amateur'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :<json boolean active: Description: Activate the account so you can start using it., Default: True, Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>json boolean active: Description: Activate the account so you can start using it., Default: True, Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :<json boolean blocked: Description: As a manager, you need to specifically accept the user by unblocking it's account., Default: True, Roles with writing permission: ('admin', 'superuser')
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
   :>json string role: Allowed: {'basic', 'superuser', 'admin', 'employee', 'amateur'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :>json boolean active: Description: Activate the account so you can start using it., Default: True, Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
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
   :>json string \*@type: Allowed: {'Account'}
   :>json list fingerprints: Read only: True
   :>json string role: Allowed: {'basic', 'superuser', 'admin', 'employee', 'amateur'}, Default: basic, Roles with writing permission: ('admin', 'superuser'), Doc: See the Roles section to get more info.
   :>json boolean active: Description: Activate the account so you can start using it., Default: True, Doc: Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.
   :>json boolean blocked: Description: As a manager, you need to specifically accept the user by unblocking it's account., Default: True, Roles with writing permission: ('admin', 'superuser')
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
   :<json string \*@type: Allowed: {'Add'}
   :<json list->Device components: Description: Components affected by the event.
   :<json url sameAs: 
   :<json string->Device \*device: 
   :>json string \*@type: Allowed: {'Add'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string label: Description: A short, descriptive title
   :<json email \*unregisteredTo.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :<json string unregisteredTo.name: Description: The name of an account, if it is a person or an organization.
   :<json dict unregisteredTo: 
   :<json boolean unregisteredTo.isOrganization: 
   :<json objectid->Account to: Excludes: unregisteredTo, OR: ['unregisteredTo']
   :<json string unregisteredTo.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :<json string \*@type: Allowed: {'Allocate'}
   :<json boolean undefinedDate: Description: Check this to say: "This owner possessed the device for an undetermined amount of time"., Default: False, Excludes: date
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Allocate'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'Deallocate'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Deallocate'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :>jsonarr string pid: Unique: True
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr string labelId: 
   :>jsonarr hid hid: 
   :>jsonarr string _id: Unique: True
   :>jsonarr string model: 
   :>jsonarr string serialNumber: 
   :>jsonarr string manufacturer: 
   :>jsonarr float memory: Unit Code: mbyte (4L)
   :>jsonarr string productId: 
   :>jsonarr list->Account owners: Read only: True
   :>jsonarr objectid->Place place: Read only: True
   :>jsonarr integer size: Unit Code: mbyte (4L)
   :>jsonarr integer numberOfCores: 
   :>jsonarr list->Device components: Default: []
   :>jsonarr list->Event erasures: Read only: True
   :>jsonarr string type: Allowed: {'HUB', 'Microtower', 'MultifunctionPrinter', 'Netbook', 'Server', 'Mouse', 'TFT', 'Printer', 'Router', 'SAI', 'Terminal', 'Scanner', 'LCD', 'Laptop', 'Keyboard', 'Desktop', 'Switch'}
   :>jsonarr boolean forceCreation: Default: False
   :>jsonarr integer maxAcceptedMemory: 
   :>jsonarr integer usedSlots: 
   :>jsonarr string imei: Unique: True
   :>jsonarr url url: Read only: True
   :>jsonarr string meid: Unique: True
   :>jsonarr dict_of_TestHardDrive test: 
   :>jsonarr natural inches: 
   :>jsonarr string \*@type: Allowed: {'SoundCard', 'HardDrive', 'Mobile', 'Device', 'RamModule', 'Component', 'GraphicCard', 'MobilePhone', 'Processor', 'Peripheral', 'Motherboard', 'Computer', 'NetworkAdapter', 'ComputerMonitor', 'TabletComputer', 'OpticalDrive'}
   :>jsonarr boolean isUidSecured: Default: True
   :>jsonarr list_of_BenchmarkHardDrive benchmarks: Read only: True
   :>jsonarr string->Device parent: 
   :>jsonarr integer totalSlots: 
   :>jsonarr dict connectors: 
   :>jsonarr natural connectors.firewire: 
   :>jsonarr natural connectors.usb: 
   :>jsonarr natural connectors.pcmcia: 
   :>jsonarr natural connectors.serial: 
   :>jsonarr boolean public: Default: False
   :>jsonarr list->Event tests: Read only: True
   :>jsonarr url sameAs: 
   :>jsonarr float width: Unit Code: m (MTR)
   :>jsonarr float height: Unit Code: m (MTR)
   :>jsonarr integer blockSize: 
   :>jsonarr float speed: Unit Code: mhz (MHZ)
   :>jsonarr string firmwareRevision: 
   :>jsonarr string interface: 
   :>jsonarr float weight: Unit Code: kgm (KGM)
   :>jsonarr integer sectors: 
   :>jsonarr integer address: Allowed: {256, 32, 64, 128, 8, 16}, Unit Code: bit (A99)
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
 

.. http:post:: (string:database)/devices



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
   :<json string pid: Unique: True
   :<json string label: Description: A short, descriptive title
   :<json string labelId: 
   :<json hid hid: 
   :>json string label: Description: A short, descriptive title
   :>json hid hid: 
   :>json string pid: Unique: True
   :<json string _id: Unique: True
   :<json string model: 
   :<json string serialNumber: 
   :<json string manufacturer: 
   :<json float memory: Unit Code: mbyte (4L)
   :<json string productId: 
   :<json integer size: Unit Code: mbyte (4L)
   :<json integer numberOfCores: 
   :<json list_of_Component->Device components: Default: []
   :<json string type: Allowed: {'HUB', 'Microtower', 'MultifunctionPrinter', 'Netbook', 'Server', 'Mouse', 'TFT', 'Printer', 'Router', 'SAI', 'Terminal', 'Scanner', 'LCD', 'Laptop', 'Keyboard', 'Desktop', 'Switch'}
   :<json boolean forceCreation: Default: False
   :<json integer maxAcceptedMemory: 
   :<json integer usedSlots: 
   :<json string imei: Unique: True
   :<json string meid: Unique: True
   :<json dict_of_TestHardDrive test: 
   :<json natural inches: 
   :<json dict_of_EraseBasic erasure: Write only: True
   :<json string \*@type: Allowed: {'SoundCard', 'HardDrive', 'Mobile', 'Device', 'RamModule', 'Component', 'GraphicCard', 'MobilePhone', 'Processor', 'Peripheral', 'Motherboard', 'Computer', 'NetworkAdapter', 'ComputerMonitor', 'TabletComputer', 'OpticalDrive'}
   :<json boolean isUidSecured: Default: True
   :<json dict_of_BenchmarkHardDrive benchmark: Write only: True
   :<json string->Device parent: 
   :<json integer totalSlots: 
   :<json dict connectors: 
   :<json natural connectors.firewire: 
   :<json natural connectors.usb: 
   :<json natural connectors.pcmcia: 
   :<json natural connectors.serial: 
   :<json boolean public: Default: False
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'SoundCard', 'HardDrive', 'Mobile', 'Device', 'RamModule', 'Component', 'GraphicCard', 'MobilePhone', 'Processor', 'Peripheral', 'Motherboard', 'Computer', 'NetworkAdapter', 'ComputerMonitor', 'TabletComputer', 'OpticalDrive'}
   :<json float width: Unit Code: m (MTR)
   :<json float height: Unit Code: m (MTR)
   :<json integer blockSize: 
   :<json float speed: Unit Code: mhz (MHZ)
   :<json string firmwareRevision: 
   :<json string interface: 
   :<json float weight: Unit Code: kgm (KGM)
   :<json integer sectors: 
   :<json integer address: Allowed: {256, 32, 64, 128, 8, 16}, Unit Code: bit (A99)
   :<json string description: Description: Full long description
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

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
   :>json string label: Description: A short, descriptive title
   :>json string labelId: 
   :>json hid hid: 
   :>json string _id: Unique: True
   :>json string model: 
   :>json string serialNumber: 
   :>json string manufacturer: 
   :>json float memory: Unit Code: mbyte (4L)
   :>json string productId: 
   :>json list->Account owners: Read only: True
   :>json objectid->Place place: Read only: True
   :>json integer size: Unit Code: mbyte (4L)
   :>json integer numberOfCores: 
   :>json list->Device components: Default: []
   :>json list->Event erasures: Read only: True
   :>json string type: Allowed: {'HUB', 'Microtower', 'MultifunctionPrinter', 'Netbook', 'Server', 'Mouse', 'TFT', 'Printer', 'Router', 'SAI', 'Terminal', 'Scanner', 'LCD', 'Laptop', 'Keyboard', 'Desktop', 'Switch'}
   :>json boolean forceCreation: Default: False
   :>json integer maxAcceptedMemory: 
   :>json integer usedSlots: 
   :>json string imei: Unique: True
   :>json url url: Read only: True
   :>json string meid: Unique: True
   :>json dict_of_TestHardDrive test: 
   :>json natural inches: 
   :>json string \*@type: Allowed: {'SoundCard', 'HardDrive', 'Mobile', 'Device', 'RamModule', 'Component', 'GraphicCard', 'MobilePhone', 'Processor', 'Peripheral', 'Motherboard', 'Computer', 'NetworkAdapter', 'ComputerMonitor', 'TabletComputer', 'OpticalDrive'}
   :>json boolean isUidSecured: Default: True
   :>json list_of_BenchmarkHardDrive benchmarks: Read only: True
   :>json string->Device parent: 
   :>json integer totalSlots: 
   :>json dict connectors: 
   :>json natural connectors.firewire: 
   :>json natural connectors.usb: 
   :>json natural connectors.pcmcia: 
   :>json natural connectors.serial: 
   :>json boolean public: Default: False
   :>json list->Event tests: Read only: True
   :>json url sameAs: 
   :>json float width: Unit Code: m (MTR)
   :>json float height: Unit Code: m (MTR)
   :>json integer blockSize: 
   :>json float speed: Unit Code: mhz (MHZ)
   :>json string firmwareRevision: 
   :>json string interface: 
   :>json float weight: Unit Code: kgm (KGM)
   :>json integer sectors: 
   :>json integer address: Allowed: {256, 32, 64, 128, 8, 16}, Unit Code: bit (A99)
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
   :>json string \*@type: Allowed: {'SoundCard', 'HardDrive', 'Mobile', 'Device', 'RamModule', 'Component', 'GraphicCard', 'MobilePhone', 'Processor', 'Peripheral', 'Motherboard', 'Computer', 'NetworkAdapter', 'ComputerMonitor', 'TabletComputer', 'OpticalDrive'}
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
   :<json string \*@type: Allowed: {'Dispose'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Dispose'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'EraseSectors', 'EraseBasic'}
   :<json list steps: 
   :<json string \*steps.@type: Allowed: {'Random', 'Zeros'}
   :<json datetime steps.endingTime: 
   :<json datetime steps.startingTime: 
   :<json boolean steps.secureRandomSteps: 
   :<json boolean \*steps.success: 
   :<json boolean steps.cleanWithZeros: 
   :<json datetime startingTime: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :<json boolean cleanWithZeros: 
   :<json natural \*secureRandomSteps: 
   :<json boolean success: 
   :<json url sameAs: 
   :<json datetime endingTime: 
   :<json string->Device \*device: 
   :>json string \*@type: Allowed: {'EraseSectors', 'EraseBasic'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'EraseSectors'}
   :<json list steps: 
   :<json string \*steps.@type: Allowed: {'Random', 'Zeros'}
   :<json datetime steps.endingTime: 
   :<json datetime steps.startingTime: 
   :<json boolean steps.secureRandomSteps: 
   :<json boolean \*steps.success: 
   :<json boolean steps.cleanWithZeros: 
   :<json datetime startingTime: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :<json boolean cleanWithZeros: 
   :<json natural \*secureRandomSteps: 
   :<json boolean success: 
   :<json url sameAs: 
   :<json datetime endingTime: 
   :<json string->Device \*device: 
   :>json string \*@type: Allowed: {'EraseSectors'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :>jsonarr string label: Description: A short, descriptive title
   :>jsonarr email \*unregisteredTo.email: Unique: True
   :>jsonarr string unregisteredReceiver.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr string unregisteredTo.name: Description: The name of an account, if it is a person or an organization.
   :>jsonarr dict unregisteredReceiver: 
   :>jsonarr boolean unregisteredReceiver.isOrganization: 
   :>jsonarr objectid->Account byUser: Read only: True
   :>jsonarr objectid->Account from: 
   :>jsonarr dict unregisteredTo: 
   :>jsonarr boolean unregisteredTo.isOrganization: 
   :>jsonarr objectid->Account receiver: Excludes: unregisteredReceiver, OR: ['unregisteredReceiver']
   :>jsonarr objectid->Account to: Excludes: unregisteredTo, OR: ['unregisteredTo']
   :>jsonarr string unregisteredReceiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr string unregisteredTo.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>jsonarr list steps: 
   :>jsonarr string \*steps.@type: Allowed: {'Random', 'Zeros'}
   :>jsonarr datetime steps.endingTime: 
   :>jsonarr datetime steps.startingTime: 
   :>jsonarr boolean steps.secureRandomSteps: 
   :>jsonarr boolean \*steps.success: 
   :>jsonarr boolean steps.cleanWithZeros: 
   :>jsonarr string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :>jsonarr string byOrganization: Read only: True
   :>jsonarr dict debug: 
   :>jsonarr version version: 
   :>jsonarr boolean \*acceptedConditions: Allowed: {True}
   :>jsonarr integer firstError: 
   :>jsonarr string \*status: 
   :>jsonarr list unsecured: Default: [], Read only: True
   :>jsonarr string unsecured.@type: 
   :>jsonarr string unsecured.type: Allowed: {'model', 'pid'}
   :>jsonarr string->Device unsecured._id: 
   :>jsonarr string fromOrganization: Read only: True
   :>jsonarr natural \*secureRandomSteps: 
   :>jsonarr datetime startingTime: 
   :>jsonarr url url: Read only: True
   :>jsonarr boolean automatic: 
   :>jsonarr boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>jsonarr ['boolean'] force: 
   :>jsonarr string receiverOrganization: Read only: True
   :>jsonarr string \*@type: Allowed: {'Register', 'Deallocate', 'Allocate', 'Receive', 'Dispose', 'Event', 'Repair', 'EraseSectors', 'Free', 'EventWithDevices', 'ToRepair', 'EraseBasic', 'EventWithOneDevice', 'Snapshot', 'TestHardDrive', 'Remove', 'Locate', 'ToDispose', 'Ready', 'ToPrepare', 'Add'}
   :>jsonarr boolean offline: 
   :>jsonarr objectid->Place place: Description: Where did it happened
   :>jsonarr boolean undefinedDate: Description: Check this to say: "This owner possessed the device for an undetermined amount of time"., Default: False, Excludes: date
   :>jsonarr integer lifetime: 
   :>jsonarr list->Event events: Read only: True
   :>jsonarr boolean \*error: 
   :>jsonarr objectid->Event snapshot: 
   :>jsonarr datetime endingTime: 
   :>jsonarr boolean success: 
   :>jsonarr string->Device parent: Description: The event triggered in this computer.
   :>jsonarr dict->Device \*device: 
   :>jsonarr string toOrganization: Read only: True
   :>jsonarr boolean cleanWithZeros: 
   :>jsonarr string request: Read only: True
   :>jsonarr list->Device components: Description: Components affected by the event., Read only: True
   :>jsonarr url sameAs: 
   :>jsonarr list->Device \*devices: 
   :>jsonarr datetime date: Description: When this happened. Leave blank if it is happening now
   :>jsonarr boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>jsonarr boolean secured: Default: False
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
   :>json email \*unregisteredReceiver.email: Unique: True
   :>json string label: Description: A short, descriptive title
   :>json email \*unregisteredTo.email: Unique: True
   :>json string unregisteredReceiver.name: Description: The name of an account, if it is a person or an organization.
   :>json string unregisteredTo.name: Description: The name of an account, if it is a person or an organization.
   :>json dict unregisteredReceiver: 
   :>json boolean unregisteredReceiver.isOrganization: 
   :>json objectid->Account byUser: Read only: True
   :>json objectid->Account from: 
   :>json dict unregisteredTo: 
   :>json boolean unregisteredTo.isOrganization: 
   :>json objectid->Account receiver: Excludes: unregisteredReceiver, OR: ['unregisteredReceiver']
   :>json objectid->Account to: Excludes: unregisteredTo, OR: ['unregisteredTo']
   :>json string unregisteredReceiver.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json string unregisteredTo.organization: Description: The name of the organization the account is in. Organizations can be inside other organizations.
   :>json list steps: 
   :>json string \*steps.@type: Allowed: {'Random', 'Zeros'}
   :>json datetime steps.endingTime: 
   :>json datetime steps.startingTime: 
   :>json boolean steps.secureRandomSteps: 
   :>json boolean \*steps.success: 
   :>json boolean steps.cleanWithZeros: 
   :>json string \*type: Allowed: {'RecyclingPoint', 'FinalUser', 'CollectionPoint'}
   :>json string byOrganization: Read only: True
   :>json dict debug: 
   :>json version version: 
   :>json boolean \*acceptedConditions: Allowed: {True}
   :>json integer firstError: 
   :>json string \*status: 
   :>json list unsecured: Default: [], Read only: True
   :>json string unsecured.@type: 
   :>json string unsecured.type: Allowed: {'model', 'pid'}
   :>json string->Device unsecured._id: 
   :>json string fromOrganization: Read only: True
   :>json natural \*secureRandomSteps: 
   :>json datetime startingTime: 
   :>json url url: Read only: True
   :>json boolean automatic: 
   :>json boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :>json ['boolean'] force: 
   :>json string receiverOrganization: Read only: True
   :>json string \*@type: Allowed: {'Register', 'Deallocate', 'Allocate', 'Receive', 'Dispose', 'Event', 'Repair', 'EraseSectors', 'Free', 'EventWithDevices', 'ToRepair', 'EraseBasic', 'EventWithOneDevice', 'Snapshot', 'TestHardDrive', 'Remove', 'Locate', 'ToDispose', 'Ready', 'ToPrepare', 'Add'}
   :>json boolean offline: 
   :>json objectid->Place place: Description: Where did it happened
   :>json boolean undefinedDate: Description: Check this to say: "This owner possessed the device for an undetermined amount of time"., Default: False, Excludes: date
   :>json integer lifetime: 
   :>json list->Event events: Read only: True
   :>json boolean \*error: 
   :>json objectid->Event snapshot: 
   :>json datetime endingTime: 
   :>json boolean success: 
   :>json string->Device parent: Description: The event triggered in this computer.
   :>json dict->Device \*device: 
   :>json string toOrganization: Read only: True
   :>json boolean cleanWithZeros: 
   :>json string request: Read only: True
   :>json list->Device components: Description: Components affected by the event., Read only: True
   :>json url sameAs: 
   :>json list->Device \*devices: 
   :>json datetime date: Description: When this happened. Leave blank if it is happening now
   :>json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :>json boolean secured: Default: False
   :>json string comment: Description: Short comment for fast and easy reading
   :>json string description: Description: Full long description
   :>json point geo: Description: Where did it happened, Excludes: place, OR: ['place']
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
   :<json string \*@type: Allowed: {'Free'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Free'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'Locate'}
   :<json objectid->Place place: Description: Where did it happened
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Locate'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened, Excludes: place, OR: ['place']
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
   :>jsonarr string \*@type: Allowed: {'Place'}
   :>jsonarr url url: Read only: True
   :>jsonarr list->Device devices: Default: []
   :>jsonarr string type: Allowed: {'Zone', 'CollectionPoint', 'Warehouse', 'Department'}
   :>jsonarr objectid->Account byUser: Read only: True
   :>jsonarr url sameAs: 
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
   :<json list->Device devices: Default: []
   :<json string type: Allowed: {'Zone', 'CollectionPoint', 'Warehouse', 'Department'}
   :<json url sameAs: 
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
   :>json string \*@type: Allowed: {'Place'}
   :>json url url: Read only: True
   :>json list->Device devices: Default: []
   :>json string type: Allowed: {'Zone', 'CollectionPoint', 'Warehouse', 'Department'}
   :>json objectid->Account byUser: Read only: True
   :>json url sameAs: 
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
   :>json string \*@type: Allowed: {'Place'}
   :>json list->Device devices: Default: []
   :>json string type: Allowed: {'Zone', 'CollectionPoint', 'Warehouse', 'Department'}
   :>json url sameAs: 
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
   :<json string \*@type: Allowed: {'Ready'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Ready'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'Receive'}
   :<json objectid->Place place: Description: Where did it happened
   :<json boolean \*acceptedConditions: Allowed: {True}
   :<json list->Device \*devices: 
   :<json boolean automaticallyAllocate: Description: Allocates to the user, Default: False
   :<json string \*type: Allowed: {'CollectionPoint', 'FinalUser', 'RecyclingPoint'}
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Receive'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'Register'}
   :<json objectid->Place place: Description: Where did it happened
   :<json list_of_Component->Device components: 
   :<json ['boolean'] force: 
   :<json url sameAs: 
   :<json dict_of_Device->Device device: 
   :>json string \*@type: Allowed: {'Register'}
   :>json dict_of_Device->Device device: 
   :>json list_of_Component->Device components: 
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'Remove'}
   :<json list->Device components: Description: Components affected by the event.
   :<json url sameAs: 
   :<json string->Device \*device: 
   :>json string \*@type: Allowed: {'Remove'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'Repair'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Repair'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

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
   :<json string \*@type: Allowed: {'Snapshot'}
   :<json version version: 
   :<json dict debug: 
   :<json objectid->Place place: Description: Where did it happened
   :<json dict_of_Device->Device \*device: 
   :<json boolean automatic: 
   :<json list_of_Component->Device components: Default: []
   :<json boolean offline: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'Snapshot'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json boolean secured: Default: False
   :<json string description: Description: Full long description
   :<json string comment: Description: Short comment for fast and easy reading
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
   :<json string \*@type: Allowed: {'TestHardDrive'}
   :<json objectid->Event snapshot: 
   :<json string->Device parent: Description: The event triggered in this computer.
   :<json integer lifetime: 
   :<json integer firstError: 
   :<json string \*status: 
   :<json string type: 
   :<json boolean \*error: 
   :<json url sameAs: 
   :<json string->Device \*device: 
   :>json string \*@type: Allowed: {'TestHardDrive'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'ToDispose'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'ToDispose'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'ToPrepare'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'ToPrepare'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
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
   :<json string \*@type: Allowed: {'ToRepair'}
   :<json list->Device \*devices: 
   :<json url sameAs: 
   :>json string \*@type: Allowed: {'ToRepair'}
   :<json datetime date: Description: When this happened. Leave blank if it is happening now
   :<json boolean secured: Default: False
   :<json boolean incidence: Description: Check if something went wrong, you can add details in a comment, Default: False
   :<json string comment: Description: Short comment for fast and easy reading
   :<json string description: Description: Full long description
   :<json point geo: Description: Where did it happened
   :>json datetime _updated:
   :>json datetime _created:
   :>json dict _links: Provides `HATEOAS` directives. In concrete a link to *itself*, the *parent* endpoint and the *collection* endpoint. See http://python-eve.org/features.html#hateoas.
 

