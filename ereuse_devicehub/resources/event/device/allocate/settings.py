import copy

from ereuse_devicehub.resources.account.settings import unregistered_user, unregistered_user_doc
from ereuse_devicehub.resources.event.device.settings import components, EventWithDevices, \
    EventSubSettingsMultipleDevices


class Allocate(EventWithDevices):
    to = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'schema': unregistered_user,
        'doc': 'The user the devices are allocated to. ' + unregistered_user_doc,
        'get_from_data_relation_or_create': 'email',
        'required': True,
        'sink': 2
    }
    toOrganization = {
        'type': 'string',
        'readonly': True,
        'materialized': True,
        'doc': 'Materialization of the organization that, by the time of the allocation, the user worked in.'
    }
    components = copy.deepcopy(components)


Allocate.components['readonly'] = True


class AllocateSettings(EventSubSettingsMultipleDevices):
    _schema = Allocate
    fa = 'fa-hand-o-right'
    sink = -5
    extra_response_fields = EventSubSettingsMultipleDevices.extra_response_fields + ['to']
    short_description = 'Assign the devices to someone, so that person \'owns\' the device'

# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it
