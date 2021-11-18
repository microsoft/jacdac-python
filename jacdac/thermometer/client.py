# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class ThermometerClient(Client):
    """
    A thermometer measuring outside or inside environment.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_THERMOMETER, JD_THERMOMETER_PACK_FORMATS, role)
    

    @property
    def temperature(self) -> Optional[float]:
        """
        The temperature., °C
        """
        reg = self.register(JD_THERMOMETER_REG_TEMPERATURE)
        value = reg.value(0)
        return cast(Optional[float], value)

    @property
    def min_temperature(self) -> Optional[float]:
        """
        Lowest temperature that can be reported., °C
        """
        reg = self.register(JD_THERMOMETER_REG_MIN_TEMPERATURE)
        value = reg.value(0)
        return cast(Optional[float], value)

    @property
    def max_temperature(self) -> Optional[float]:
        """
        Highest temperature that can be reported., °C
        """
        reg = self.register(JD_THERMOMETER_REG_MAX_TEMPERATURE)
        value = reg.value(0)
        return cast(Optional[float], value)

    @property
    def temperature_error(self) -> Optional[float]:
        """
        The real temperature is between `temperature - temperature_error` and `temperature + temperature_error`., °C
        """
        reg = self.register(JD_THERMOMETER_REG_TEMPERATURE_ERROR)
        value = reg.value(0)
        return cast(Optional[float], value)

    @property
    def variant(self) -> Optional[ThermometerVariant]:
        """
        (Optional) Specifies the type of thermometer.
        """
        reg = self.register(JD_THERMOMETER_REG_VARIANT)
        value = reg.value(0)
        return cast(Optional[ThermometerVariant], value)

    
