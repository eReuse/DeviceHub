import copy

from app.event.settings import event_sub_settings_multiple_devices, components, EventWithDevices, \
    EventSubSettingsMultipleDevices


class Deallocate(EventWithDevices):
    _from = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'sink': 2
    }
    fromOrganization = {
    # Materialization of the organization that, by the time of the deallocation, the user worked in
        'type': 'string',
        'readonly': True
    }

    @staticmethod
    def _clean(full_dict):
        super()._clean(full_dict)
        full_dict['from'] = full_dict['_from']
        del full_dict['_from']


Deallocate.components = copy.deepcopy(components)
Deallocate.components['readonly'] = True


# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

class DeallocateSettings(EventSubSettingsMultipleDevices):
    _schema = Deallocate
