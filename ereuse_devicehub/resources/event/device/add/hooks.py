from flask import current_app as app


def add_components(events: dict):
    """
    Adds the new devices to the materialized attribute 'components' of the parent device.
    """
    for event in events:
        app.data.driver.db['devices'].update(
            {'_id': event['device']},
            {'$addToSet': {'components': {'$each': event['components']}}}
        )


def delete_components(resource_name: str, add: dict):
    if add.get('@type') == 'devices:Add':
        app.data.driver.db['devices'].update(
            {'_id': add['device']},
            {'$pull': {'components': {'$in': add['components']}}}
        )
