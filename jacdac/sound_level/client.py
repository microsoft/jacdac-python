# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class SoundLevelClient(SensorClient):
    """
    A sound level detector sensor, gives a relative indication of the sound level.
    Implements a client for the `Sound level <https://microsoft.github.io/jacdac-docs/services/soundlevel>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_sound_level_value: float = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SOUND_LEVEL, JD_SOUND_LEVEL_PACK_FORMATS, role)
        self.missing_sound_level_value = missing_sound_level_value

    @property
    def sound_level(self) -> Optional[float]:
        """
        The sound level detected by the microphone, _: /
        """
        self.refresh_reading()
        return self.register(JD_SOUND_LEVEL_REG_SOUND_LEVEL).float_value(self.missing_sound_level_value, 100)

    @property
    def enabled(self) -> Optional[bool]:
        """
        Turn on or off the microphone., 
        """
        return self.register(JD_SOUND_LEVEL_REG_ENABLED).bool_value()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.register(JD_SOUND_LEVEL_REG_ENABLED).set_values(value)


    
