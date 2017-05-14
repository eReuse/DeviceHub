from collections import defaultdict, OrderedDict

import flask_excel as excel
from eve.auth import requires_auth
from flask import current_app
from flask import request
from pydash import keys
from pydash import map_
from pydash import py_
from pyexcel_webio import FILE_TYPE_MIME_TABLE as REVERSED_FILE_TYPE_MIME_TABLE
from werkzeug.exceptions import NotAcceptable

from ereuse_devicehub.header_cache import header_cache
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.resources.submitter.translator import Translator
from ereuse_devicehub.rest import execute_get

FILE_TYPE_MIME_TABLE = dict(zip(REVERSED_FILE_TYPE_MIME_TABLE.values(), REVERSED_FILE_TYPE_MIME_TABLE.keys()))


@header_cache(expires=10)
@requires_auth('resource')
def export(db, resource):
    """
    Exports devices as spreadsheets.
    See the docs in non-resource-endpoints.rst
    """
    try:
        file_type = FILE_TYPE_MIME_TABLE[request.accept_mimetypes.best]
    except KeyError:
        raise NotAcceptable()
    ids = request.args.getlist('ids')
    token = AccountDomain.hash_token(AccountDomain.actual_token)
    translator = SpreadsheetTranslator()
    spreadsheets = OrderedDict()
    if resource in Group.resource_names:
        domain = GroupDomain.children_resources[resource]
        f = py_().select(lambda d: d['@type'] not in Component.types and not d.get('placeholder', False)).map('_id')
        # ids are groups and we want their inner devices, each of them in a page:
        # page1 is group1 and contains its devices, page2 is group2 and contains its devices, and so on
        for label in ids:
            devices = domain.get_descendants(DeviceDomain, label)
            # We fetch again devices as we want them embedded
            spreadsheets[label] = translator.translate(get_devices(f(devices), db, token))
    else:
        spreadsheets['Devices'] = translator.translate(get_devices(ids, db, token))
    return excel.make_response_from_book_dict(spreadsheets, file_type, file_name=resource)


def get_devices(ids, db, token) -> list:
    # todo this is limited by pagination; redo with get_internal when updating python eve
    PAGINATION_LIMIT = current_app.config['PAGINATION_LIMIT']
    params = {'where': {'_id': {'$in': ids}}, 'embedded': {'components': 1}, 'max_results': PAGINATION_LIMIT}
    return execute_get(db + '/devices', token, params=params)['_items']


class SpreadsheetTranslator(Translator):
    def __init__(self):
        # Definition of the dictionary used to translate
        p = py_()
        d = OrderedDict()  # we want ordered dict as in translate we want to get the keys in this order
        d['Identifier'] = p.get('_id')
        d['Label ID'] = p.get('labelId')
        d['Serial Number'] = p.get('serialNumber')
        d['Model'] = p.get('model')
        d['Manufacturer'] = p.get('manufacturer')
        d['Actual State'] = p.get('events').first().pick('@type', 'label', '_id').implode(' ')
        d['Registered in'] = p.get('_created')
        d['Processor'] = p.get('processorModel')
        d['RAM (GB)'] = p.get('totalRamSize').floor()
        d['HDD (MB)'] = p.get('totalHardDriveSize').floor()
        # Note that in translate_one we translate 'components'
        super().__init__(d)

    def translate(self, resources: list) -> list:
        """Translates a spreadsheet, which is a table of resources as rows plus the field names as header."""
        translated = super().translate(resources)
        # Let's transform the dict to a table-like array
        # Generation of table headers
        field_names = list(self.dict.keys())  # We want first the keys we set in the translation dict
        field_names += py_(translated).map(keys).flatten().uniq().difference(field_names).sort().value()
        # compute the rows; header titles + fields (note we do not use pick as we don't want None but '' for empty)
        return [field_names] + map_(translated, lambda res: [res.get(f, '') or '' for f in field_names])

    def translate_one(self, resource: dict) -> dict:
        translated = super().translate_one(resource)

        # Translation of 'components'
        component_translation = py_().pick('_id', 'serialNumber', 'model', 'manufacturer').implode(' ')
        components = map_(resource.get('components', {}), lambda c: component_translation(c))
        # Let's decompose components so we get ComponentTypeA 1: ..., ComponentTypeA 2: ...
        counter_each_type = defaultdict(int)
        for pos, translated_component in enumerate(components):
            component_type = resource['components'][pos]['@type']
            count = counter_each_type[component_type] = counter_each_type[component_type] + 1
            translated['{} {}'.format(component_type, count)] = translated_component
        return translated
