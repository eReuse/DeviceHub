from ereuse_devicehub.resources.event.device.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Add(EventWithOneDevice):
    components = components


class AddSettings(EventSubSettingsOneDevice):
    _schema = Add
    glyphicon = 'fa-plus-square-o'
    short_description = 'Components have been added to a device'
    item_methods = ['GET']
