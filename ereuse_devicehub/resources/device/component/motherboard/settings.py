from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings


class Motherboard(Component):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.totalSlots = {
            'type': 'integer',
            'teaser': False
        }
        self.usedSlots = {
            'type': 'integer',
            'teaser': False
        }
        self.connectors = {
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
        self.maxAcceptedMemory = {
            'type': 'integer',  # Maximum accepted memory that the motherboard can hold
            'teaser': False
        }


class MotherboardSettings(ComponentSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = Motherboard
        self.etag_ignore_fields = parent.etag_ignore_fields + ['usedSlots']
