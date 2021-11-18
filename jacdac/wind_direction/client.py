# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class WindDirectionClient(Client):
    """
    A sensor that measures wind direction.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_WIND_DIRECTION, JD_WIND_DIRECTION_PACK_FORMATS, role)
    

    @property
    def wind_direction(self) -> Optional[int]:
        """
        The direction of the wind., _: °
        """
        reg = self.register(JD_WIND_DIRECTION_REG_WIND_DIRECTION)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @property
    def wind_direction_error(self) -> Optional[int]:
        """
        (Optional) Error on the wind direction reading, _: °
        """
        reg = self.register(JD_WIND_DIRECTION_REG_WIND_DIRECTION_ERROR)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    
