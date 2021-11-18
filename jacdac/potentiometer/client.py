from jacdac.bus import Bus, Client
from .constants import *
from typing import Union


class PotentiometerClient(Client):
    """
    A slider or rotary potentiometer.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_POTENTIOMETER, JD_POTENTIOMETER_PACK_FORMATS, role)
    

    @property
    def position(self) -> Union[float, None]:
        """
        The relative position of the slider., /
        """
        reg = self.register(JD_POTENTIOMETER_REG_POSITION)
        return reg.value(0)

    @property
    def variant(self) -> Union[PotentiometerVariant, None]:
        """
        (Optional) Specifies the physical layout of the potentiometer.
        """
        reg = self.register(JD_POTENTIOMETER_REG_VARIANT)
        return reg.value(0)

    
