# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class WindSpeedClient(SensorClient):
    """
    A sensor that measures wind speed.
    Implements a client for the `Wind speed <https://microsoft.github.io/jacdac-docs/services/windspeed>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_wind_speed_value: float = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_WIND_SPEED, JD_WIND_SPEED_PACK_FORMATS, role, preferred_interval = 60000)
        self.missing_wind_speed_value = missing_wind_speed_value

    @property
    def wind_speed(self) -> Optional[float]:
        """
        The velocity of the wind., _: m/s
        """
        self.refresh_reading()
        return self.register(JD_WIND_SPEED_REG_WIND_SPEED).value(self.missing_wind_speed_value)

    @property
    def wind_speed_error(self) -> Optional[float]:
        """
        (Optional) Error on the reading, _: m/s
        """
        return self.register(JD_WIND_SPEED_REG_WIND_SPEED_ERROR).value()

    @property
    def max_wind_speed(self) -> Optional[float]:
        """
        (Optional) Maximum speed that can be measured by the sensor., _: m/s
        """
        return self.register(JD_WIND_SPEED_REG_MAX_WIND_SPEED).value()

    
