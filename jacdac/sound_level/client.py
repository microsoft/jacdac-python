# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class SoundLevelClient(Client):
    """
    A sound level detector sensor, gives a relative indication of the sound level.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SOUND_LEVEL, JD_SOUND_LEVEL_PACK_FORMATS, role)
    

    @property
    def sound_level(self) -> Optional[float]:
        """
        The sound level detected by the microphone, _: /
        """
        reg = self.register(JD_SOUND_LEVEL_REG_SOUND_LEVEL)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def enabled(self) -> Optional[bool]:
        """
        Turn on or off the microphone., 
        """
        reg = self.register(JD_SOUND_LEVEL_REG_ENABLED)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        reg = self.register(JD_SOUND_LEVEL_REG_ENABLED)
        reg.set_values(value) # type: ignore


    @property
    def min_decibels(self) -> Optional[int]:
        """
        (Optional) The minimum power value considered by the sensor.
        If both ``min_decibels`` and ``max_decibels`` are supported,
        the volume in deciment can be linearly interpolated between
        ``[min_decibels, max_decibels]``., _: dB
        """
        reg = self.register(JD_SOUND_LEVEL_REG_MIN_DECIBELS)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @min_decibels.setter
    def min_decibels(self, value: int) -> None:
        reg = self.register(JD_SOUND_LEVEL_REG_MIN_DECIBELS)
        reg.set_values(value) # type: ignore


    @property
    def max_decibels(self) -> Optional[int]:
        """
        (Optional) The maximum power value considered by the sensor.
        If both ``min_decibels`` and ``max_decibels`` are supported,
        the volume in deciment can be linearly interpolated between
        ``[min_decibels, max_decibels]``., _: dB
        """
        reg = self.register(JD_SOUND_LEVEL_REG_MAX_DECIBELS)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @max_decibels.setter
    def max_decibels(self, value: int) -> None:
        reg = self.register(JD_SOUND_LEVEL_REG_MAX_DECIBELS)
        reg.set_values(value) # type: ignore


    @property
    def loud_threshold(self) -> Optional[float]:
        """
        The sound level to trigger a loud event., _: /
        """
        reg = self.register(JD_SOUND_LEVEL_REG_LOUD_THRESHOLD)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @loud_threshold.setter
    def loud_threshold(self, value: float) -> None:
        reg = self.register(JD_SOUND_LEVEL_REG_LOUD_THRESHOLD)
        reg.set_values(value) # type: ignore


    @property
    def quiet_threshold(self) -> Optional[float]:
        """
        The sound level to trigger a quiet event., _: /
        """
        reg = self.register(JD_SOUND_LEVEL_REG_QUIET_THRESHOLD)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @quiet_threshold.setter
    def quiet_threshold(self, value: float) -> None:
        reg = self.register(JD_SOUND_LEVEL_REG_QUIET_THRESHOLD)
        reg.set_values(value) # type: ignore


    def on_loud(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Raised when a loud sound is detected
        """
        return self.on_event(JD_SOUND_LEVEL_EV_LOUD, handler)

    def on_quiet(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Raised when a period of quietness is detected
        """
        return self.on_event(JD_SOUND_LEVEL_EV_QUIET, handler)

    
