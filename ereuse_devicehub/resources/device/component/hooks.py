def del_blacklist(_: str, items: list):
    for item in items:
        if '_blacklist' in item:
            del item['_blacklist']