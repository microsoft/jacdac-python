# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class WaterLevelClient(Client):
    """
    A sensor that measures liquid/water level.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_WATER_LEVEL, JD_WATER_LEVEL_PACK_FORMATS, role)
    

    @property
    def level(self) -> Optional[float]:
        """
        The reported water level., _: /
        """
        reg = self.register(JD_WATER_LEVEL_REG_LEVEL)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def variant(self) -> Optional[WaterLevelVariant]:
        """
        (Optional) The type of physical sensor., 
        """
        reg = self.register(JD_WATER_LEVEL_REG_VARIANT)
        values = reg.values()
        return cast(Optional[WaterLevelVariant], values[0] if values else None)

    
