import copy

from app.device.component.settings import component_sub_settings, Component, ComponentSubSettings

sound_card_settings = copy.deepcopy(component_sub_settings)


class SoundCard(Component):
    pass


class SoundCardSettings(ComponentSubSettings):
    _schema = SoundCard
