import copy

from app.device.component.settings import component_sub_settings, Component, ComponentSubSettings

optical_drive_settings = copy.deepcopy(component_sub_settings)


class OpticalDrive(Component):
    pass


class OpticalDriveSettings(ComponentSubSettings):
    _schema = OpticalDrive
