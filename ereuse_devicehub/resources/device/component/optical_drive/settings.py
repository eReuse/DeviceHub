from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings


class OpticalDrive(Component):
    pass


class OpticalDriveSettings(ComponentSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = OpticalDrive
