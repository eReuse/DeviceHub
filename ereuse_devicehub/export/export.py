from collections import defaultdict
from math import floor

import flask_excel as excel
from eve.auth import requires_auth
from flask import current_app
from flask import json
from flask import request
from pyexcel_webio import FILE_TYPE_MIME_TABLE as REVERSED_FILE_TYPE_MIME_TABLE
from sortedcontainers import SortedSet
from werkzeug.exceptions import NotAcceptable

from ereuse_devicehub.flask_decorators import crossdomain
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.submitter.translator import ResourceTranslator, ResourcesTranslator
from ereuse_devicehub.rest import execute_get

FILE_TYPE_MIME_TABLE = dict(zip(REVERSED_FILE_TYPE_MIME_TABLE.values(), REVERSED_FILE_TYPE_MIME_TABLE.keys()))


@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@requires_auth('resource')
def export(db, resource):
    try:
        file_type = FILE_TYPE_MIME_TABLE[request.accept_mimetypes.best]
    except KeyError:
        raise NotAcceptable()
    ids = request.args.getlist('ids')
    token = AccountDomain.hash_token(AccountDomain.actual_token)
    group_by = request.args.get('groupBy')
    default_group = request.args.get('defaultGroup', 'Others')
    embedded = {'byUser': 1, 'events': 1, 'components': 1, 'owners': 1}  # todo we do not get places for now 'place': 1
    translator = SpreadsheetTranslator(current_app.config, group_by=group_by, default_group=default_group)
    exporter = Exporter(translator, embedded, token)
    spreadsheets, _ = exporter.export(ids, db, resource)[0]
    return excel.make_response_from_book_dict(spreadsheets, file_type, file_name=resource)


class Exporter:
    def __init__(self, translator: ResourcesTranslator, embedded: dict, token=None):
        self.translator = translator
        self.embedded = embedded
        self.token = token

    def export(self, resources_id: list, database: str or None, resource_name: str):
        where = json.dumps({'_id': {'$in': resources_id}})
        embedded = json.dumps(self.embedded)
        url = '{}/{}{}'.format(database, resource_name, '?where={}&embedded={}'.format(where, embedded))
        resources = execute_get(url, self.token)['_items']
        return self.translator.translate(resources)


class SpreadsheetResourceTranslator(ResourceTranslator):
    def __init__(self, config, generic_dict: dict = None, specific_dict: dict = None, **kwargs):
        inner_fields = ['_id', 'serialNumber', 'model', 'manufacturer']
        generic_dict = generic_dict or {
            'Identifier': (self.identity, '_id'),
            'Label ID': (self.identity, 'labelId'),
            'Serial Number': (self.identity, 'serialNumber'),
            'Model': (self.identity, 'model'),
            'Manufacturer': (self.identity, 'manufacturer'),
            # 'Actual place': (self.inner_field('label'), 'place'), todo we do not get places for now
            'Actual state': (self.nth_resource(0, after=self.inner_fields(['@type', 'label', '_id'])), 'events'),
            'Registered in': (self.identity, '_created'),
            'Created by': (self.inner_field('email'), 'byUser'),
            'CPU': (self.identity, 'processorModel'),
            'RAM (GB)': (floor, 'totalRamSize'),
            'HDD (MB)': (floor, 'totalHardDriveSize'),
            'components': (self.for_all(self.inner_fields(inner_fields)),)
        }
        super().__init__(config, generic_dict, specific_dict, **kwargs)

    def _translate(self, resource: dict) -> dict:
        """As super but decomposing each component to a column (Graphic Card 1, Graphic Card 2...)"""
        translated = super()._translate(resource)
        counter_each_type = defaultdict(int)
        for pos, translated_component in enumerate(translated['components']):
            component_type = resource['components'][pos]['@type']
            count = counter_each_type[component_type] = counter_each_type[component_type] + 1
            translated['{} {}'.format(component_type, count)] = translated_component
        del translated['components']
        return translated


class SpreadsheetTranslator(ResourcesTranslator):
    def __init__(self, config: dict, resource_translator: SpreadsheetResourceTranslator = None,
                 generic_dict: dict = None, specific_dict: dict = None, group_by: dict = None, default_group='Others',
                 **kwargs):
        self.group_by = group_by
        self.default_group = default_group
        resource_translator = resource_translator or SpreadsheetResourceTranslator(config)
        super().__init__(config, resource_translator, generic_dict, specific_dict, **kwargs)

    def _translate(self, resources: list) -> dict:
        """
        Given a list of id of resources, transforms them to Flask-Excel's
        `book dict <http://flask-excel.readthedocs.io/en/latest/#flask_excel.make_response_from_book_dict>`_.
        with the following structure:

        {
            'group1': [[row1], [row2], [row3]...],
            'group2: [[row1], [row2], [row3]...]
        }
        """
        resources = self._translate_resources(resources)
        # We get all the field names, note that not all field_names are in all resources
        # And we want the 'static_field_names' to be before other fields
        field_names = ['Label ID', 'Identifier', 'Serial Number', 'Model', 'Manufacturer', 'CPU', 'RAM (GB)',
                       'HDD (MB)']
        other_field_names = SortedSet()
        for resource, _ in resources:
            other_field_names = other_field_names | resource.keys()
        field_names += list(other_field_names - set(field_names))
        spreadsheet = defaultdict(list)
        for resource, _ in resources:
            row = [resource.get(field_name, '') for field_name in field_names]
            group = resource.get(self.group_by, self.default_group)
            spreadsheet[group].append(row)
            if len(spreadsheet[group]) == 1:
                spreadsheet[group].insert(0, list(field_names))
        return spreadsheet
