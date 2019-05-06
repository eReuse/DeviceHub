import pymongo
from collections import Iterator, OrderedDict, defaultdict
from contextlib import suppress
from datetime import timedelta

import flask_excel as excel
from eve.auth import requires_auth
from flask import request
from inflection import humanize
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from pydash import keys, map_, py_
from pyexcel_webio import FILE_TYPE_MIME_TABLE as REVERSED_FILE_TYPE_MIME_TABLE
from werkzeug.exceptions import NotAcceptable

from ereuse_devicehub.header_cache import header_cache
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.resources.submitter.translator import Translator

FILE_TYPE_MIME_TABLE = dict(zip(REVERSED_FILE_TYPE_MIME_TABLE.values(), REVERSED_FILE_TYPE_MIME_TABLE.keys()))


@header_cache(expires=10)
@requires_auth('resource')
def export(db, resource):
    """
    Exports devices as spreadsheets.
    See the docs in other-endpoints.rst
    """
    try:
        file_type = FILE_TYPE_MIME_TABLE[request.accept_mimetypes.best]
    except KeyError:
        raise NotAcceptable()
    ids = request.args.getlist('ids')  # Returns empty list by default
    translator = SpreadsheetTranslator(
        request.args.get('type', 'detailed') == 'brief',
        request.args.get('max-of-type', None, type=int)
    )
    spreadsheets = OrderedDict()
    if resource in Group.resource_names:
        domain = GroupDomain.children_resources[resource]
        f = py_().filter(lambda d: d['@type'] not in Component.types and not d.get('placeholder', False))
        # ids are groups and we want their inner devices, each of them in a page:
        # page1 is group1 and contains its devices, page2 is group2 and contains its devices, and so on
        for _id in ids:
            group = domain.get_one(_id)
            # Let's get the full devices and their components with embedded stuff
            devices = f(domain.get_descendants(DeviceDomain, _id))
            devices_with_components = map(_get_device_with_components, devices)
            spreadsheets[group.get('label', group['_id'])] = translator.translate(devices_with_components)
    else:
        # Let's get the full devices and their components with embedded stuff
        QUERY = {'@type': {'$nin': Component.types}}
        devices = DeviceDomain.get_in('_id', ids, False) if ids else DeviceDomain.get(QUERY, False)
        devices_with_components = map(_get_device_with_components, devices)
        spreadsheets['Devices'] = translator.translate(devices_with_components)
    return excel.make_response_from_book_dict(spreadsheets, file_type, file_name=resource)


def _get_device_with_components(device):
    if 'components' in device:
        device['components'] = DeviceDomain.get_full_components(device['components'])
    else:
        device['components'] = []
    return device


class SpreadsheetTranslator(Translator):
    """Translates a set of devices into a dict for flask-excel representing a spreadsheet"""

    def __init__(self, brief: bool, max_components_of_type=None):
        # Definition of the dictionary used to translate
        self.brief = brief
        self.max_components_of_type = max_components_of_type
        p = py_()
        d = OrderedDict()  # we want ordered dict as in translate we want to preserve this order in the spreadsheet
        d['Identifier'] = p.get('_id')
        d['Type'] = p.get('@type')
        d['Subtype'] = p.get('type')
        if not brief:
            d['Label ID'] = p.get('labelId')
            d['Giver ID'] = p.get('gid')
            d['Platform ID'] = p.get('pid')
            d['Refurbisher ID'] = p.get('rid')
            d['Serial Number'] = p.get('serialNumber')
        d['Price'] = p.get('pricing.total.standard')
        d['Price 2 years warranty'] = p.get('pricing.total.warranty2')
        d['Model'] = p.get('model')
        d['Manufacturer'] = p.get('manufacturer')
        if not brief:
            d['State'] = p.get('events').head().pick('@type', 'label').join(' ')
            d['Registered in'] = p.get('_created')
        d['Processor'] = p.get('processorModel')
        d['RAM (GB)'] = p.get('totalRamSize').floor()
        d['HDD (MB)'] = p.get('totalHardDriveSize').floor()
        d['Condition Score'] = p.get('condition.general.score')
        d['Condition'] = p.get('condition.general.range')
        if not brief:
            d['Appearance'] = p.get('condition.appearance.general')
            d['Appearance Score'] = p.get('condition.appearance.score')
            d['Functionality'] = p.get('condition.functionality.general')
            d['Functionality Score'] = p.get('condition.functionality.score')
            d['Labelling'] = p.get('condition.labelling')
            d['Bios'] = p.get('condition.bios.general')
            d['Processor Score'] = p.get('condition.components.processors')
            d['RAM Score'] = p.get('condition.components.ram')
            d['HDD Score'] = p.get('condition.components.hardDrives')
            d['Refurbisher percentage'] = p.get('pricing.refurbisher.standard.percentage')
            d['Refurbisher amount'] = p.get('pricing.refurbisher.standard.amount')
            d['Retailer percentage'] = p.get('pricing.retailer.standard.percentage')
            d['Retailer amount'] = p.get('pricing.retailer.standard.amount')
            d['Platform percentage'] = p.get('pricing.platform.standard.percentage')
            d['Platform amount'] = p.get('pricing.platform.standard.amount')
            d['Refurbisher percentage 2 years warranty'] = p.get('pricing.refurbisher.warranty2.percentage')
            d['Refurbisher amount 2 years warranty'] = p.get('pricing.refurbisher.warranty2.amount')
            d['Retailer percentage 2 years warranty'] = p.get('pricing.retailer.warranty2.percentage')
            d['Retailer amount 2 years warranty'] = p.get('pricing.retailer.warranty2.amount')
            d['Platform percentage 2 years warranty'] = p.get('pricing.platform.warranty2.percentage')
            d['Platform amount 2 years warranty'] = p.get('pricing.platform.warranty2.amount')
        # Note that in translate_one we translate 'components'
        super().__init__(d)

    def translate_one(self, device: dict) -> dict:
        translated = super().translate_one(device)
        # Avoid exception in openpyxl/cell/cell.py line 156 for using illegal characters
        for key, value in translated.items():
            if type(value) is str:
                if next(ILLEGAL_CHARACTERS_RE.finditer(value), None):
                    translated[key] = '**'
        # Component translation
        # Let's decompose components so we get ComponentTypeA 1: ..., ComponentTypeA 2: ...
        pick = py_().pick(([] if self.brief else ['_id', 'serialNumber']) + ['model', 'manufacturer']).join(' ')
        counter_each_type = defaultdict(int)
        for pos, component in enumerate(device['components']):
            _type = device['components'][pos]['@type']
            count = counter_each_type[_type] = counter_each_type[_type] + 1
            if self.max_components_of_type and count >= self.max_components_of_type:
                continue
            header = '{} {}'.format(_type, count)
            translated[header + ' system id'] = component.get('_id', '')
            translated[header + ' serial number'] = component.get('serialNumber', '')
            translated[header + ' model'] = component.get('model', '')
            translated[header + ' manufacturer'] = component.get('manufacturer', '')
            if not self.brief or _type not in {'Motherboard', 'RamModule', 'Processor'}:
                translated[header] = pick(component)
                if _type == 'HardDrive':
                    with suppress(KeyError):
                        erasure = component['erasures'][0]
                        t = '{} {}'.format('Successful' if erasure['success'] else 'Failed', humanize(erasure['@type']))
                        translated[header + ' erasure'] = t
                    with suppress(KeyError):
                        lifetime = round(timedelta(hours=component['tests'][0]['lifetime']).days / 365, 2)
                        translated[header + ' lifetime (years)'] = lifetime
                        translated[header + ' test result'] = component['tests'][0]['status']
                        # For david
                        translated[header + ' lifetime (hours)'] = component['tests'][0]['lifetime']
                        translated[header + ' reading speed'] = component['benchmarks'][0]['readingSpeed']
                        translated[header + ' writing speed'] = component['benchmarks'][0]['writingSpeed']
                elif _type == 'Processor':
                    with suppress(KeyError):
                        translated[header + ' number of cores'] = component['numberOfCores']
                    with suppress(KeyError):
                        translated[header + ' score'] = next(b['score'] for b in component['benchmarks'] if b['@type'] == 'BenchmarkProcessor')
                elif _type == 'RamModule':
                    for field in 'size', 'speed':
                        with suppress(KeyError):
                            translated[header + ' ' + field] = component[field]
        if translated.get('Registered in', None):
            # When snapshot executes this method devices don't have this property
            translated['Registered in'] = str(translated['Registered in'])

        # Update event
        if not self.brief:
            with suppress(EventNotFound):
                updates = DeviceEventDomain.get({'$query': {'devices': {'$in': [device['_id']]}, '@type': 'devices:Update'},
                                                        '$orderby': {'_created': pymongo.ASCENDING}})
                for update in updates:
                    if update.get('margin', None):
                        translated['Margin'] = update['margin']
                    if update.get('price', None):
                        translated['Price Update'] = update['price']
                    if update.get('partners', None):
                        translated['Partners'] = update['partners']
                    if update.get('originNote', None):
                        translated['Origin note'] = update['originNote']
                    if update.get('targetNote', None):
                        translated['Target note'] = update['targetNote']
                    if update.get('guaranteeYears', None):
                        translated['Guarantee Years'] = update['guaranteeYears']
                    if update.get('invoicePlatformId', None):
                        translated['Invoice Platform ID'] = update['invoicePlatformId']
                    if update.get('invoiceRetailerId', None):
                        translated['Invoice Retailer ID'] = update['invoiceRetailerId']
                    if update.get('eTag', None):
                        translated['eTag'] = update['eTag']

            # Same as
            same_as = device.get('sameAs', None)
            if same_as:
                components = same_as[0].split('/')
                translated['Last other inventory ID'] = '{} {}'.format(components[3], components[-1])
                for url in same_as:
                    components = url.split('/')
                    translated[components[3]] = components[-1]
        return translated

    def translate(self, devices: Iterator) -> list:
        """Translates a spreadsheet, which is a table of resources as rows plus the field names as header."""
        translated = super().translate(devices)
        # Let's transform the dict to a table-like array
        # Generation of table headers
        # We want first the keys we set in the translation dict
        field_names = list(self.dict.keys())
        if not self.brief:
            field_names.extend([
                'Margin', 'Price Update', 'Partners', 'Origin note', 'Target note',
                'Guarantee Years', 'Invoice Platform ID', 'Invoice Retailer ID',
                'Last other inventory ID', 'eTag'
            ])
        field_names += py_(translated).map(keys).flatten().uniq().difference(field_names).sort().value()
        # compute the rows; header titles + fields (note we do not use pick as we don't want None but '' for empty)
        return [field_names] + map_(translated, lambda res: [res.get(f, '') if res.get(f, None) is not None else '' for f in field_names])
