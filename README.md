# DeviceHub

DeviceHub is a system to manage devices focused in reusing them (what we call a [DCMS](#device-circularity-management-system)),
created under the project [eReuse](https://www.ereuse.org).

Our main objectives are:

* To offer a common IT Asset Management for donors, receivers and IT professionals so they can manage devices and exchange them.
This is, reusing –and ultimately recycling.
* To automatically recollect, analyse, process and share (controlling privacy) metadata about devices with other tools of the
eReuse ecosystem to guarantee traceability, and to provide inputs for the indicators which measure circularity.
* To highly integrate with existing IT Asset Management Systems.
* To be decentralized.

DeviceHub is a server providing a RESTful API under JSON following the specifics of [Python-EVE](http://python-eve.org/features.html)
and designed thought to be used by JSON-LD (although we need to improve support) and Schema.org naming.

## General info
DeviceHub uses mainly 3 types of objects, with many subtypes. These are:

- Devices. From smartphones to computers. Some devices can have inner devices, called components. Both a computer and
a graphic card are devices. A graphic card is a component too, because it can be inside of a computer.
- Events, or things that happen to the devices. We never work on devices directly, but we perform
events to them. We can *Repair* a device, *Allocate* it to an employee, etc.
- Accounts, which represent users. They perform the events.

## Events
You can see a [list of all the events](https://wiki.ereuse.org/arch:events) (some not implemented yet) DeviceHub will admit.
We describe here the event *Snapshot*, which is the most used one.

#### Snapshot
A snapshot is an event that takes by parameters the actual state of a device, this is,
all its info and the info of its components. Snapshot is the event that is performed when you upload the JSON generated
by [DeviceInventory](https://github.com/eReuse/device-inventory). Do not generate the contents manually -DeviceHub will check in the near future that the info comes from DeviceInventory
and it has not been modified by the user.

DeviceHub updates the database with the changes reflected by the the devices in the snapshot, performing, if necessary, the next events:

- Register, creating a device.
- Add, adding new components to a device.
- Remove, removing components from a device.
- TestHardDrive, saving the results of the testing process of a hard drive, so it can generate a certificate.
- EraseBasic, saving the results of the erasure process of a hard drive, so it can generate a certificate.

## API
Take a look at the [API section of the wiki of DeviceHub](https://github.com/eReuse/DeviceHub/wiki/API).

## Requirements
* Python 3.4 or 3.5
* MongoDB
* pip will automatically install appropriate python packages

## Install and run

To install it just type in a console:

``pip install eReuse-DeviceHub``

And to use it:

```python
from ereuse_devicehub import DeviceHub
app = DeviceHub()
app.run()
```

## Device Circularity Management System
Device Circularity Management System comes from IT Asset Management System, which at the same time comes from IT Asset Management.

As [Gartner](http://www.gartner.com/it-glossary/it-asset-management-itam), “IT Asset Management (ITAM) entails
collecting inventory, financial and contractual data to manage the IT asset throughout its life cycle.
ITAM depends on robust processes, with tools to automate manual processes”

In our case, we offer a system to manage devices focused in reusing them (so-called [circular economy](http://www.ellenmacarthurfoundation.org/circular-economy)).
Being devices a subtype of asset, it is more specific to define our solution as a “Device Circularity Management System”.
We need to comment that we do not incorporate financial and contractual data as an objective for this project,
but as this information is useful to generate indicators about circularity, it can be future work.
