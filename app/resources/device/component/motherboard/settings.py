from app.resources.device.component.settings import Component, ComponentSubSettings


class Motherboard(Component):
    totalSlots = {
        'type': 'integer',
        'teaser': False
    }
    usedSlots = {
        'type': 'integer',
        'teaser': False
    }
    connectors = {
        'type': 'dict',
        'schema': {
            'usb': {
                'type': 'natural'
            },
            'firewire': {
                'type': 'natural'
            },
            'serial': {
                'type': 'natural'
            },
            'pcmcia': {
                'type': 'natural'
            }
        }
    }
    maxAcceptedMemory = {
        'type': 'integer',  # Maximum accepted memory that the motherboard can hold
        'teaser': False
    }


class MotherboardSettings(ComponentSubSettings):
    _schema = Motherboard
    etag_ignore_fields = ComponentSubSettings.etag_ignore_fields + ['usedSlots']
