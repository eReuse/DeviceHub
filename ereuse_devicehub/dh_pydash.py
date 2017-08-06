import pydash
from pydash import to_path


def deep_pick(obj, *properties: str, discard_falsey: bool = False) -> dict:
    """
    As pick(without callback) but for paths.Destination key is the last name of the path: for 'a.b.c' is 'c'.
    :param obj:
    :param properties:
    :param discard_falsey: Should falsey values be discarded?
    """
    ret = dict()
    for path in properties:
        dest_name = to_path(path)[-1]
        value = pydash.get(obj, path)
        if value or not discard_falsey:
            ret[dest_name] = value
    return ret


pydash.deep_pick = deep_pick
