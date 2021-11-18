from jacdac.bus import Bus, Client
from .constants import *
from typing import Union


class ThermometerClient(Client):
    """
    A thermometer measuring outside or inside environment.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_THERMOMETER, JD_THERMOMETER_PACK_FORMATS, role)

    @property
    def temperature(self) -> Union[float, None]:
        """
        The temperature., °C
        """
        reg = self.register(JD_THERMOMETER_REG_TEMPERATURE)
        return reg.value(0)

    @property
    def min_temperature(self) -> Union[float, None]:
        """
        Lowest temperature that can be reported., °C
        """
        reg = self.register(JD_THERMOMETER_REG_MIN_TEMPERATURE)
        return reg.value(0)

    @property
    def max_temperature(self) -> Union[float, None]:
        """
        Highest temperature that can be reported., °C
        """
        reg = self.register(JD_THERMOMETER_REG_MAX_TEMPERATURE)
        return reg.value(0)

    @property
    def temperature_error(self) -> Union[float, None]:
        """
        The real temperature is between `temperature - temperature_error` and `temperature + temperature_error`., °C
        """
        reg = self.register(JD_THERMOMETER_REG_TEMPERATURE_ERROR)
        return reg.value(0)

    @property
    def variant(self) -> Union[ThermometerVariant, None]:
        """
        (Optional) Specifies the type of thermometer.
        """
        reg = self.register(JD_THERMOMETER_REG_VARIANT)
        return reg.value(0)
