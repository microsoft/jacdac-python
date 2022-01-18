# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional


class SoundPlayerClient(Client):
    """
    A device that can play various sounds stored locally. This service is typically paired with a ``storage`` service for storing sounds.
    Implements a client for the `Sound player <https://microsoft.github.io/jacdac-docs/services/soundplayer>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SOUND_PLAYER, JD_SOUND_PLAYER_PACK_FORMATS, role)


    @property
    def volume(self) -> Optional[float]:
        """
        (Optional) Global volume of the output. ``0`` means completely off. This volume is mixed with each play volumes., _: /
        """
        return self.register(JD_SOUND_PLAYER_REG_VOLUME).float_value(100)

    @volume.setter
    def volume(self, value: float) -> None:
        self.register(JD_SOUND_PLAYER_REG_VOLUME).set_values(value / 100)



    def play(self, name: str) -> None:
        """
        Starts playing a sound.
        """
        self.send_cmd_packed(JD_SOUND_PLAYER_CMD_PLAY, name)

    def cancel(self, ) -> None:
        """
        Cancel any sound playing.
        """
        self.send_cmd_packed(JD_SOUND_PLAYER_CMD_CANCEL, )
    
