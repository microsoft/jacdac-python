# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class SoundPlayerClient(Client):
    """
    A device that can play various sounds stored locally. This service is typically paired with a ``storage`` service for storing sounds.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SOUND_PLAYER, JD_SOUND_PLAYER_PACK_FORMATS, role)
    

    @property
    def volume(self) -> Optional[float]:
        """
        Global volume of the output. ``0`` means completely off. This volume is mixed with each play volumes., _: /
        """
        reg = self.register(JD_SOUND_PLAYER_REG_VOLUME)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @volume.setter
    def volume(self, value: float) -> None:
        reg = self.register(JD_SOUND_PLAYER_REG_VOLUME)
        reg.set_values(value)



    def play(self, name: str) -> None:
        """
        Starts playing a sound.
        """
        self.send_cmd_packed(JD_SOUND_PLAYER_CMD_PLAY, name)
    
