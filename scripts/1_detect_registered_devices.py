"""
    Execute this script in the folder of some files, and modify the list in the main method with the registered labels
    in the system.

    This script copies in the 'found' folder the snapshots which labels where found in the giving list, and in the
    'not found' folder all thte other snapshots.

    This works with the original snapshot json file.
"""
from pprint import pprint
import os
import json
import shutil

this_directory = os.path.dirname(os.path.realpath(__file__))


def get_json_from_file(filename: str) -> dict:
    with open(os.path.abspath(os.path.join(this_directory, filename))) as data_file:
        return json.load(data_file)


def main(labels):
    not_found_files = []
    found_files = []
    nf_dest_dict = os.path.join(this_directory, 'not found')
    os.makedirs(nf_dest_dict, exist_ok=True)
    f_dest_dict = os.path.join(this_directory, 'found')
    os.makedirs(f_dest_dict, exist_ok=True)
    for filename in os.listdir('.'):
        if 'json' in filename:
            event = get_json_from_file(filename)
            label = event['label']
            if int(label) not in labels:
                not_found_files.append(filename)
                shutil.copyfile(filename, os.path.join(nf_dest_dict, filename))
            else:
                found_files.append(filename)
                shutil.copyfile(filename, os.path.join(f_dest_dict, filename))
    not_found_files.sort()
    found_files.sort()
    return not_found_files, found_files


not_found, found = main(
    (1, 12, 10, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 26, 27, 28, 3, 30, 34, 4, 42, 46, 5, 6, 7, 8, 9))
pprint("found")
pprint(found)
pprint("not found")
pprint(not_found)
pprint("Not found files copied")
