from app.device.device import Device


def materialize_actual_owners_remove(events: list):
    for event in events:
        properties = {'$pull': {'owners': event['from']}}
        Device.update(event['devices'], properties)
        Device.update(event.get('components', []), properties)