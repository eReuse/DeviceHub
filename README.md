# DeviceHub

##Installing instructions
Using wsgi / apache

1.  Install mongo, supported the latest 2.X and 3.X versions.
2.  Create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
3.  pip install inflection eve eve-docs
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
6.  Modify settings.py of DeviceHub accordingly (Mongo stuf... defaults should work for a default mongo installation)
7.  Restart apache
