Vocabulary
==========


In DeviceHub there are four main resources:

- :ref:`device`
- Event
- Place
- Account


Check in :ref: `api` how to consume the resources, or `download the formal JSON Schema with the specification of the different devices (among other resources) <https://api.devicetag.io/schema>`_,
note that you can `get here <https://github.com/eReuse/DeviceHub/blob/master/ereuse_devicehub/resources/schema.py>`_ the reference for the unit codes.


.. _device:

Device
------

Device is a meticulously chosen word by its generic definition, which represents our purpose to be able to reuse almost
anything, although we start with a subset of electronic devices. Some devices can have inner devices called components.
The relationship is recursive: as components are devices that can have inner components, too. For example, both a
computer and a graphic card are devices, and the transistors of a graphic card are devices. Although designed as
an infinite recursive, the agents in eReuse.org only support one layer of recursivity: this is Computer --> GraphicCard,
but not then GraphicCard --> transistor.

Device partly extends IndividualProduct, from Schema.org. The result is a class describing physical characteristics from a
device (width, weight...), identifiers (serial number, HID, synthetic identifier, URL...), and other metadata
(model, manufacturer name...). Device is extended by:

- :ref:`ComputerMonitor`
- :ref:`Mobile`: smartphones and tablets, for which we can record the IMEI and MEID.
- :ref:`Computer`: Desktop, laptops, servers...
- :ref:`Peripheral`: a wildcard for any “device that is used to put information into or get information out of the computer”.
- :ref:`Component`

    - :ref:`GraphicCard`: Future work is to incorporate, or to link to existing benchmarks about the model of graphic card.
    - :ref:`HardDrive`
    - :ref:`Motherboard`: We collect the types and number of connectors the motherboard has.
    - :ref:`NetworkAdapter`: (from Network Interface Controller), using the MAC Address as the identifier.
    - :ref:`OpticalDrive`: CD, DVD, HD-DVD and Blu-ray readers and recorders.
    - :ref:`Processor` (from Computer Processor).
    - :ref:`RamModule` (from Random Access Memory).
    - :ref:`SoundCard`


.. figure:: img/devicehub-diagram-products.*

   Device class diagram without components

.. figure:: img/devicehub-diagram-components.*

   Components class diagram


.. _event:

Event
-----
Events are the actions performed to resources such as devices. For example, to say to the system that a device has been
repaired, we will perform the event Repair with the concrete device as a parameter. Event extends Event from Schema.org,
with attributes defining where it happened (by defining a place or by geo-coordinates), who performed it, when (both
user defined date and system dates), and a control if the event can be considered secured (because it has been checked
by the system or it has been automatic), etcetera. DeviceHub and GRD store, such as in a log, the events performed to
a device, successfully monitoring its life cycle.

Classes extending events need to be written following the general conventions (PascalName), and they represent
a verb in the infinitive when possible. Some events represent the willingness or assignment to do an action
(ToAllocate vs Allocate, ToPrepare vs Prepare, ToDispose vs Dispose...). These verbs have the preposition *To* as
a prefix.

There are the following events:

- :ref:`devices-Accept`: The user or organization accepts the done to it. After this, the devices are assigned to it.
- :ref:`devices-Add`: A component is added to a device.
- :ref:`devices-Allocate`: The device has been assigned to a user or an organization. The allocated users or organizations are responsible for the device.
- :ref:`devices-Deallocate`: The reverse of allocate. Removes the assignation from a user or an organization.
- :ref:`devices-Dispose`: The device has been correctly disposed.
- :ref:`devices-EraseBasic`: The hard drive has been erased in a fast way. A certificate can be generated from this event.
- :ref:`Free`: A device is freed (made available) when there is willingness for it to be donated or used, and the device works correctly. Not implemented yet.
- :ref:`devices-Locate`: The device has been located.
- :ref:`devices-Migrate`: Changes the holder agent of the device. Migrate is a final state for a device in an agent. The events after migration need to come from the new agent.
- :ref:`devices-Ready`: A device is ready when it has been assured that it works correctly.
- :ref:`devices-Receive`: The receiver, a user or an organization, confirms that the device has arrived. There are the following types of reception: RecyclingPoint, CollectionPoint and FinalUser.
- :ref:`devices-Recycle`: The device has been recycled. This is the end of its lifetime.
- :ref:`devices-Register`: The device has been registered (created) on the system. This event cannot be triggered directly; use :ref:`devices-Snapshot` instead.
- :ref:`devices-Reject`: A user or an organization refuses a ToAllocate done to it.
- :ref:`devices-Remove`: A component has been removed from a device.
- :ref:`devices-Repair`: A device has been repaired.
- :ref:`devices-Snapshot`: Updates the ITAMS so the state and events of its devices are the same as the given parameters.
- :ref:`devices-TestHardDrive`: A test has been performed to a hard drive. The tests check for the integrity of the hard drive. DeviceHub can generate a certificate from the data of this event.
- :ref:`devices-ToAllocate`: Tries to allocate a device to a user in an organization. After a ToAllocate is performed: (1) user must accept it or reject, and (2) if user accepted it, the system will perform Allocate.
- :ref:`devices-ToPrepare`: A device has been selected to be prepared. Usually is the next event done after being registered.
- :ref:`devices-ToDispose`: The device must be disposed. It does not say to which collection point the device is going to be taken to, we can extrapolate this from Allocate.
- :ref:`devices-ToRepair`: A device has been selected to be repaired. This event will probably require a message for the technician to know what to repair.
- :ref:`devices-Dispose`: A device has been succesfully disposed.

Allocate, Deallocate and Receive usually present some confusion, so we explain the differences: Allocate assigns the user or organization that has some kind of property over the device. Allocate can be performed on different users, and all of them will share the property.
Deallocate removes the property from one user. On the other hand, Receive sets the device physically with the user or organization. Performing Receive again to another user will move the device to that one. The system is quite granular, and it is up to the organization to adopt a more or less rigorous way to apply the events.

.. figure:: https://www.devicetag.io/common/assets/common/components/event/event-explanation/event.svg

   An easy explanation used in DeviceTag.io to explain the most used events.

.. figure:: img/devicehub-diagram-events-with-one-device.*

   Class diagram for the Events (1)

.. figure:: img/devicehub-diagram-events-with-devices.*

   Class diagram for the Events (2)
