from importlib import import_module

import inflection as inflection
from app.accounts.User import User

__author__ = 'busta'


def get_resource_name(string: str) -> str:
    """

    :param string: String can already be a resource name, no worries.
    :return:
    """
    return inflection.dasherize(inflection.underscore(string))


def register_sub_types(domain: dict, parent_type: str, types_to_register=()):
    for type_c in types_to_register:
        type_u = inflection.underscore(type_c)
        settings = import_module('.' + type_u + '.settings', parent_type)
        getattr(settings, type_u + '_settings')['schema']['@type']['allowed'] = [type_c]
        domain.update({get_resource_name(type_c): getattr(settings, type_u + '_settings')})

def set_byUser(resource_name: str, items: list):
    from app.app import app
    if 'byUser' in app.config['DOMAIN'][resource_name]['schema']:
        for item in items:
            item['byUser'] = User.actual['_id']


def difference(new_list: list, old_list: list) ->list:
    """
    Computes the difference between two lists of values
    :param new_list: List which we want the values from
    :param old_list: List to check against
    :return:
    """
    diff = []
    for x in new_list:
        found = False
        for y in old_list:
            if x == y:
                found = True
        if not found:
            diff.append(x)
    return diff
