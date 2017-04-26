import argparse

import requests

from ereuse_devicehub.security.request_auth import Auth


def create_placeholders_and_migrate(base_url, email, password, n_placeholders, origin_db, dest_db, label=None,
                                    comment=None):
    """
       Remotely connects to a devicehub, creates n_placeholders placeholders and then migrates them to a dest_db
       in the same devicehub.
    """
    auth = Auth(base_url, email, password)
    snapshot = {
        "@type": "devices:Register",
        "device": {
            "@type": "Device",
            "placeholder": True
        }
    }

    devices_id = []
    for _ in range(0, n_placeholders):
        r = requests.post('{}/{}/events/devices/register'.format(base_url, origin_db), json=snapshot, auth=auth)
        r.raise_for_status()
        result = r.json()
        devices_id.append(result['device'])

    migrate = {
        "@type": "devices:Migrate",
        "label": label,
        "to": {
            "baseUrl": "https://devicehub.ereuse.org/",
            "database": dest_db
        },
        'devices': devices_id,
        "comment": comment
    }
    r = requests.post('{}/{}/events/devices/migrate'.format(base_url, origin_db), json=migrate, auth=auth)
    r.raise_for_status()


if __name__ == '__main__':
    desc = 'Creates a number of placeholders and then migrates them to another database. ' \
           'This method executes remotely to any DeviceHub on the web.'
    epilog = 'Example: python register_ph_migrate.py http://api.foo.bar a@a.a pass 25 db1 db2' \
             ' -l "Migrate to DB2" -c "This migrate represents..."'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument('base_url', help='Ex: https://api.devicetag.io')
    parser.add_argument('email')
    parser.add_argument('password')
    parser.add_argument('n_placeholders', help='Number of placeholders to create and migrate', type=int)
    parser.add_argument('origin_db', help='Name of the database where placeholders are Registered and them moved from')
    parser.add_argument('dest_db', help='Destination db')
    parser.add_argument('-l', '--label')
    parser.add_argument('-c', '--comment')
    args = vars(parser.parse_args())  # If --help or -h or wrong value this will print message to user and abort
    create_placeholders_and_migrate(**args)
