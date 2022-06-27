# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class AirPressureClient(SensorClient):
    """
    A sensor measuring air pressure of outside environment.
    Implements a client for the `Air Pressure <https://microsoft.github.io/jacdac-docs/services/airpressure>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_pressure_value: Optional[float] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_AIR_PRESSURE, JD_AIR_PRESSURE_PACK_FORMATS, role, preferred_interval = 60000)
        self.missing_pressure_value = missing_pressure_value

    @property
    def pressure(self) -> Optional[float]:
        """
        The air pressure., _: hPa
        """
        self.refresh_reading()
        return self.register(JD_AIR_PRESSURE_REG_PRESSURE).value(self.missing_pressure_value)

    @property
    def pressure_error(self) -> Optional[float]:
        """
        (Optional) The real pressure is between `pressure - pressure_error` and `pressure + pressure_error`., _: hPa
        """
        return self.register(JD_AIR_PRESSURE_REG_PRESSURE_ERROR).value()

    
