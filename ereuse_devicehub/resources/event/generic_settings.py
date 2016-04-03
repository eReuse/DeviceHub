from ereuse_devicehub.resources.event.event import Event
from ereuse_devicehub.resources.event.settings import EventWithDevices, EventSubSettingsMultipleDevices

"""
    Registers the generic types for the events.

    This module creates as many Schema (extending from EventWithDevices) and Settings (extending from
    EventSubSettingsMultipleDevices) as generic types are.
"""

for generic_type in Event.get_generic_types():
    # Although it is not very pythonic to register in globals, we are doing so at initialization
    globals()[generic_type] = type(generic_type, (EventWithDevices,), {})
    generic_type_settings = '{}Settings'.format(generic_type)
    globals()[generic_type_settings] = type(
        generic_type_settings,
        (EventSubSettingsMultipleDevices,),
        {'_schema': globals()[generic_type]}
    )
