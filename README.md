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

## Requirements
* Python (3.4)
* Python-Eve
* MongoDB
* Inflection (Python package)
* If you want to generate a visual representation of the API, you will need eve-docs package


## Installation
Using wsgi / apache

1.  Prepare Python 3 environment
1.  Install mongo, supported the latest 2.X and 3.X versions.
2.  Create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
3.  ``pip install inflection eve eve-docs``
4.  configure a [virtualhost](http://ubuntuforums.org/showthread.php?t=794248#post_4958995)
    ```
    # DeviceHub WSGI configuration #
    WSGIPythonPath /home/ereuse/sites/devicehub.ereuse.net/source:/home/ereuse/sites/devicehub.ereuse.net/virtualenv/lib/python3.4/site-packages

    <VirtualHost *:80>
        ServerName devicehub.ereuse.net
        ServerAlias deviceware.ereuse.net

        WSGIScriptAlias / /home/ereuse/sites/devicehub.ereuse.net/source/DeviceHub.wsgi
        WSGIDaemonProcess DeviceHubNet threads=5
        #  pass the required headers through to the application
        WSGIPassAuthorization On

        <Directory /home/ereuse/sites/devicehub.ereuse.net/source>
                WSGIProcessGroup DeviceHubNet
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
            <Files DeviceHub.wsgi>
                Require all granted
            </Files>
        </Directory>
    </VirtualHost>
    ```
5.  Create a WSGI file, for example:
    ```python
    import os, sys

    sys.path.append('/home/ereuse/sites/devicehub.ereuse.net/source')
    PROJECT_DIR =  '/home/ereuse/sites/devicehub.ereuse.net/source'
    sys.path.insert(0, PROJECT_DIR)

    sys.argv[0] = '/home/ereuse/sites/devicehub.ereuse.net/source/DeviceHub.py'

    def execfile(filename):
        globals = dict( __file__ = filename )
        exec( open(filename).read(), globals )

    execfile( '/home/ereuse/sites/devicehub.ereuse.net/virtualenv/bin/activate_this.py')
    from DeviceHub import app as application
    ```
6.  Modify settings.py of DeviceHub accordingly (defaults should work for a MongoDB installation)
7.  Restart apache


## Device Circularity Management System
Device Circularity Management System comes from IT Asset Management System, which at the same time comes from IT Asset Management.

As [Gartner](http://www.gartner.com/it-glossary/it-asset-management-itam), “IT Asset Management (ITAM) entails
collecting inventory, financial and contractual data to manage the IT asset throughout its life cycle.
ITAM depends on robust processes, with tools to automate manual processes”

In our case, we offer a system to manage devices focused in reusing them (so-called [circular economy](http://www.ellenmacarthurfoundation.org/circular-economy)).
Being devices a subtype of asset, it is more specific to define our solution as a “Device Circularity Management System”.
We need to comment that we do not incorporate financial and contractual data as an objective for this project,
but as this information is useful to generate indicators about circularity, it can be future work.
