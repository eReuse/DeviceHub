from ereuse_devicehub.resources.account.user import User
from ereuse_devicehub.resources.device.domain import DeviceDomain


def materialize_actual_owners_remove(events: list):
    for event in events:
        properties = {'$pull': {'owners': event['from']}}
        DeviceDomain.update_raw(event['devices'], properties)
        DeviceDomain.update_raw(event.get('components', []), properties)


def set_organization(deallocates: list):
    for deallocate in deallocates:
        org = User.get(deallocate['from'])['organization']
        if org is not None:
            deallocate['fromOrganization'] = org
