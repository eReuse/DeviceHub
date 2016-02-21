from app.account.user import User
from app.device.device import Device


def materialize_actual_owners_remove(events: list):
    for event in events:
        properties = {'$pull': {'owners': event['from']}}
        Device.update(event['devices'], properties)
        Device.update(event.get('components', []), properties)


def set_organization(deallocates: list):
    for deallocate in deallocates:
        org = User.get(deallocate['from'])['organization']
        if org is not None:
            deallocate['fromOrganization'] = org