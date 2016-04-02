import copy

from ereuse_devicehub.resources.event.settings import components, EventWithDevices, \
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

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        full_dict = super(Deallocate, cls)._clean(attributes, attributes_to_remove)
        full_dict['from'] = full_dict['_from']
        del full_dict['_from']
        return full_dict


Deallocate.components = copy.deepcopy(components)
Deallocate.components['readonly'] = True


# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

class DeallocateSettings(EventSubSettingsMultipleDevices):
    _schema = Deallocate
