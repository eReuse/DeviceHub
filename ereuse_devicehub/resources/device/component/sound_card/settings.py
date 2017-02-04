from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings


class SoundCard(Component):
    pass


class SoundCardSettings(ComponentSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = SoundCard
