from ereuse_devicehub.resources.event.device.domain import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import EventWithDevices, EventSubSettingsMultipleDevices, \
    materialized_components
from ereuse_devicehub.resources.resource import Resource

"""
    Registers the generic types for the events.

    This module creates as many Schema (extending from EventWithDevices) and Settings (extending from
    EventSubSettingsMultipleDevices) as generic types are.
"""

for generic_type, settings in DeviceEventDomain.GENERIC_TYPES.items():
    schema = {'components': materialized_components}
    Resource.create(generic_type, EventWithDevices, schema, EventSubSettingsMultipleDevices, settings)
