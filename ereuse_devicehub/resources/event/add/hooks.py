from ereuse_devicehub.app import app


def add_components(events: dict):
    """
    Adds the new devices to the materialized attribute 'components' of the parent device.
    """
    for event in events:
        app.data.driver.db['devices'].update(
            {'_id': event['device']},
            {'$addToSet': {'components': {'$each': event['components']}}}
        )
