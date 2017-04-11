import copy

from ereuse_devicehub.resources.event.device.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Add(EventWithOneDevice):
    components = components
    device = copy.copy(EventWithOneDevice.device)
    device['placeholder_disallowed'] = True


class AddSettings(EventSubSettingsOneDevice):
    _schema = Add
    fa = 'fa-plus-square-o'
    short_description = 'Components have been added to a device'
    item_methods = ['GET']
