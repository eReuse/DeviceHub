from ereuse_devicehub.resources.account.domain import AccountDomain, UserNotFound
from ereuse_devicehub.resources.device.domain import DeviceDomain


def materialize_actual_owners_remove(events: list):
    for event in events:
        properties = {'$pull': {'owners': event['from']}}
        DeviceDomain.update_raw(event.get('components', []), properties)
        return DeviceDomain.update_raw(event['devices'], properties)


def set_organization(deallocates: list):
    for deallocate in deallocates:
        try:
            deallocate['fromOrganization'] = AccountDomain.get_one(deallocate['from'])['organization']
        except (UserNotFound, KeyError):  # todo ensure organization is not always needed
            pass
