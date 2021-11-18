from jacdac.bus import Bus, Client
from .constants import *
from typing import Union


class BarometerClient(Client):
    """
    A sensor measuring air pressure of outside environment.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_BAROMETER, JD_BAROMETER_PACK_FORMATS, role)

    @property
    def pressure(self) -> Union[float, None]:
        """
        The air pressure., hPa
        """
        reg = self.register(JD_BAROMETER_REG_PRESSURE)
        return reg.value(0)

    @property
    def pressure_error(self) -> Union[float, None]:
        """
        The real pressure is between `pressure - pressure_error` and `pressure + pressure_error`., hPa
        """
        reg = self.register(JD_BAROMETER_REG_PRESSURE_ERROR)
        return reg.value(0)