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
                'type': 'integer'
            },
            'firewire': {
                'type': 'integer'
            },
            'serial': {
                'type': 'integer'
            },
            'pcmcia': {
                'type': 'integer'
            }
        }
    }
}
)

motherboard_settings = copy.deepcopy(component_sub_settings)

motherboard_settings.update({
    'schema': motherboard,
    'url': component_sub_settings['url'] + 'motherboard'
})
