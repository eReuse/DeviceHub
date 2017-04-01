import copy

from ereuse_devicehub.resources.event.device.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Remove(EventWithOneDevice):
    components = components
    device = copy.copy(EventWithOneDevice.device)
    device['placeholder_disallowed'] = True


class RemoveSettings(EventSubSettingsOneDevice):
    _schema = Remove
    fa = 'fa-minus-square-o'
    short_description = 'Components have been removed from a device'
    item_methods = ['GET']
