from app.app import app


def remove_components(events: dict):
    """
    Removes the components from the materialized attribute 'components' of the parent device.
    """
    for event in events:
        app.data.driver.db['devices'].update(
            {'_id': event['device']},
            {'$pull': {'components': {'$in': event['components']}}}
        )
