__author__ = 'Xavier Bustamante Talavera'
from app.device.settings import device, device_settings

component = dict(device, **{

})

component_settings = {
    'resource_methods': device_settings['resource_methods'],
    'schema': component,
    'additional_lookup': device_settings['additional_lookup'],
    'datasource': {
        'source': 'devices',
        'filter': {'@type': {'$in': ['graphicCard', 'hardDrive', 'motherboard',
                                     'networkAdapter', 'processor', 'ramModule', 'soundCard']}}
    },
    'url': device_settings['url'] + '/components/<regex("[a-f0-9]{24}"):component>'
}
