from ereuse_devicehub.resources.event.device.snapshot.snapshot import Snapshot


class MigrateCreator(Snapshot):
    def execute(self):
        """Like Snapshot's one, but removing everything related with tests and erasures"""
        event_log = []
        self.register(event_log)
        for component in self.components:
            self.get_add_remove(component, self.device)
        self._remove_nonexistent_components()
        return event_log + self.events.process()

    def get_tests_and_erasures(self, components):
        raise NotImplementedError()

    def exec_hard_drive_events(self, event_log, events):
        raise NotImplementedError()
