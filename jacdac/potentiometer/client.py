from jacdac.bus import Bus, Client
from .constants import *
from typing import Union, cast


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
        value = reg.value(0)
        return cast(Union[float, None], value)

    @property
    def variant(self) -> Union[PotentiometerVariant, None]:
        """
        (Optional) Specifies the physical layout of the potentiometer.
        """
        reg = self.register(JD_POTENTIOMETER_REG_VARIANT)
        value = reg.value(0)
        return cast(Union[PotentiometerVariant, None], value)

    
