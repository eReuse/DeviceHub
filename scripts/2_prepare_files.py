"""
This script is thought to run in a folder with JSON with the objective of:
- Add the json files to the test suite
- Make JSON devices anonymous by replacing S/N with hash values. Hash values are injective methods.
- Detect special characters in HID fields (S/N, model, manufacturer) which would cause a problem
"""
import hashlib
import json
import os
from collections import defaultdict, OrderedDict
from pprint import pprint

HID_FIELDS = 'serialNumber', 'manufacturer', 'model'
chars = defaultdict(OrderedDict)
words = defaultdict(list)
this_directory = os.path.dirname(os.path.realpath(__file__))


def get_json_from_file(filename: str) -> dict:
    with open(os.path.abspath(os.path.join(this_directory, filename))) as data_file:
        return json.load(data_file)


def sanitize(value: str, key: str) -> str:
    for char in value:
        chars[key][char] = chars[key][char] + 1 if char in chars[key] else 0
    words[key].append(value)
    if key == 'serialNumber':
        return hashlib.sha224(value.encode()).hexdigest()
    else:
        return value


def sanitize_event(d: dict):
    """
    Modified from http://stackoverflow.com/a/11700817
    :param d:
    :return:
    """
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = sanitize_event(v)
        elif k == 'components':
            new_v = []
            for lv in v:
                new_v.append(sanitize_event(lv))
            v = new_v
        elif k in HID_FIELDS:
            v = sanitize(v, k)
        new[k] = v
    return new


def main():
    dest_dict = os.path.join(this_directory, 'new')
    os.makedirs(dest_dict, exist_ok=True)
    for filename in os.listdir('.'):
        if 'json' in filename:
            event = get_json_from_file(filename)
            del event['debug']
            new_event = sanitize_event(event)
            with open(os.path.join(dest_dict, new_event['label'] + '.json'), 'xt') as f:
                f.write(json.dumps(new_event))
    with open(os.path.join(dest_dict, 'chars.txt'), 'xt') as f:
        pprint(chars, f)
    with open(os.path.join(dest_dict, 'words.txt'), 'xt') as f:
        pprint(words, f)


main()
