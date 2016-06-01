from ereuse_devicehub.resources.event.event import Event
from ereuse_devicehub.resources.event.settings import EventWithDevices, EventSubSettingsMultipleDevices
from ereuse_devicehub.resources.resource import Resource

"""
    Registers the generic types for the events.

    This module creates as many Schema (extending from EventWithDevices) and Settings (extending from
    EventSubSettingsMultipleDevices) as generic types are.
"""

for generic_type in Event.get_generic_types():
    Resource.create(generic_type, EventWithDevices, {}, EventSubSettingsMultipleDevices, {})
