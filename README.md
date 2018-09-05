# DeviceHub

DeviceHub is an IT Asset Management System focused in reusing devices,
created under the project [eReuse.org](https://www.ereuse.org).

Our main objectives are:

* To offer a common IT Asset Management for donors, receivers and IT professionals so they can manage devices and exchange them.
This is, reusing –and ultimately recycling.
* To automatically recollect, analyse, process and share (controlling privacy) metadata about devices with other tools of the
eReuse ecosystem to guarantee traceability, and to provide inputs for the indicators which measure circularity.
* To highly integrate with existing IT Asset Management Systems.
* To be decentralized.

DeviceHub is a server providing a RESTful API extending [Eve](http://python-eve.org/features.html).

## General info
DeviceHub uses mainly 3 types of objects, with many subtypes. These are:

- Devices. From smartphones to computers. Some devices can have inner devices, called components. Both a computer and
a graphic card are devices. A graphic card is a component too, because it can be inside of a computer.
- Events, or things that happen to the devices. We never work on devices directly, but we perform
events to them. We can *Repair* a device, *Allocate* it to an employee, etc.
- Accounts, which represent users. They perform the events.

## Installation

### Requirements
* Python 3.5 or newer.
* MongoDB 3.4 or newer.
* R. For debian install ``r-base``, ``python3-rpy2``, ``build-essential``,
  ``libcurl4-gnutls-dev``, ``libxml2-dev``, ``libssl-dev``
* Weasyprint requires some system packages. 
  [Their docs explain which ones and how to install them](http://weasyprint.readthedocs.io/en/stable/install.html).


### Installing

After installing the above requirements, type in a console:

```bash
    pip3 install git+https://github.com/eReuse/DeviceHub.git
```

### Running

And to use it create a python file with the following and run it:

```python
from ereuse_devicehub import DeviceHub
app = DeviceHub()
app.run()
```

### Testing
Ensure first you have the requirements of the above section.

To test it, download it from git through `git clone ...` and execute the following in the project directory:
 `python3 setup.py test`. This will install everything required for running the tests and execute them. 
