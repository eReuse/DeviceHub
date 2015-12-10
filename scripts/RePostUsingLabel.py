from app.app import app


class RePostUsingLabel:
    is_active = False
    collection = []
    db = app.data.driver.db

    @classmethod
    def activate(cls):
        cls.is_active = True

    @classmethod
    def deactivate(cls):
        cls.is_active = False

    @classmethod
    def get_devices_and_labels(cls):
        snapshots = cls.db.events.find({'@type': 'snapshot'})
        for snapshot in snapshots:
            cls.collection.append((cls.db.devices.find_one({snapshot['device']}), snapshot['label']))

    @classmethod
    def drop(cls):
        cls.db.events.drop()
        cls.db.devices.drop()

