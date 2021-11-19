# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class LightLevelClient(Client):
    """
    A sensor that measures luminosity level.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_LIGHT_LEVEL, JD_LIGHT_LEVEL_PACK_FORMATS, role)
    

    @property
    def light_level(self) -> Optional[float]:
        """
        Detect light level, _: /
        """
        reg = self.register(JD_LIGHT_LEVEL_REG_LIGHT_LEVEL)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def variant(self) -> Optional[LightLevelVariant]:
        """
        (Optional) The type of physical sensor., 
        """
        reg = self.register(JD_LIGHT_LEVEL_REG_VARIANT)
        values = reg.values()
        return cast(Optional[LightLevelVariant], values[0] if values else None)

    