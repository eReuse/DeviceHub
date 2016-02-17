import copy
from app.account.settings import unregistered_user
from app.device.settings import device
from app.event.settings import event_with_one_device, event_sub_settings_one_device, place

register = copy.deepcopy(event_with_one_device)
register.update({
    'device': {
        'type': ['dict', 'string'],
        'schema': device  # anyof causes a bug where resource is not set
    },
    'components': {
        'type': ['string', 'list'],
    },
    'force': {
        'type': ['boolean']  # Creates a device even if it does not have pid or hid, doesn't affect components
        # An automatic way of generating pid must be set (ex: PID_AS_AUTOINCREMENT)
    },
})
register.update(copy.deepcopy(place))


register_settings = copy.deepcopy(event_sub_settings_one_device)
register_settings.update({
    'resource_methods': ['POST'],
    'schema': register,
    'url': event_sub_settings_one_device['url'] + 'register',
    'extra_response_fields': ['device', 'components']
})
register_settings['datasource']['filter'] = {'@type': {'$eq': 'Register'}}
