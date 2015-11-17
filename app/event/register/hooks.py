from app.app import app


def set_components(events: dict):
    """
    Sets the new devices to the materialized attribute 'components' of the parent device.
    """
    for event in events:
        app.data.driver.db['devices'].update(
            {'_id': event['device']},
            {'$set': {'components': event['components']}}
        )
