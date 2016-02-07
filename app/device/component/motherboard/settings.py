import copy

from app.device.component.settings import component, component_sub_settings

motherboard = copy.deepcopy(component)
motherboard.update({
    'totalSlots': {
        'type': 'integer'
    },
    'usedSlots': {
        'type': 'integer'
    },
    'connectors': {
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
    },
    'maxAcceptedMemory': {
        'type': 'integer'  # Maximum accepted memory that the motherboard can hold
    }
}
)

motherboard_settings = copy.deepcopy(component_sub_settings)

motherboard_settings.update({
    'schema': motherboard,
    'url': component_sub_settings['url'] + 'motherboard',
    'etag_ignore_fields': motherboard_settings['etag_ignore_fields'] + ['usedSlots']
})
