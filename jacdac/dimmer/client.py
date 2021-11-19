# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class DimmerClient(Client):
    """
    A light or fan controller that dims the current on a line.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_DIMMER, JD_DIMMER_PACK_FORMATS, role)
    

    @property
    def intensity(self) -> Optional[float]:
        """
        The intensity of the current. Set to ``0`` to turn off completely the current., _: /
        """
        reg = self.register(JD_DIMMER_REG_INTENSITY)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @intensity.setter
    def intensity(self, value: float) -> None:
        reg = self.register(JD_DIMMER_REG_INTENSITY)
        reg.set_values(value)


    @property
    def variant(self) -> Optional[DimmerVariant]:
        """
        (Optional) The type of physical device, 
        """
        reg = self.register(JD_DIMMER_REG_VARIANT)
        values = reg.values()
        return cast(Optional[DimmerVariant], values[0] if values else None)

    