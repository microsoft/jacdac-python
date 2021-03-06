# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional, Tuple


class GyroscopeClient(SensorClient):
    """
    A 3-axis gyroscope.
    Implements a client for the `Gyroscope <https://microsoft.github.io/jacdac-docs/services/gyroscope>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_rotation_rates_value: Optional[Tuple[float, float, float]] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_GYROSCOPE, JD_GYROSCOPE_PACK_FORMATS, role)
        self.missing_rotation_rates_value = missing_rotation_rates_value

    @property
    def rotation_rates(self) -> Optional[Tuple[float, float, float]]:
        """
        Indicates the current rates acting on gyroscope., x: °/s,y: °/s,z: °/s
        """
        self.refresh_reading()
        return self.register(JD_GYROSCOPE_REG_ROTATION_RATES).value(self.missing_rotation_rates_value)

    @property
    def rotation_rates_error(self) -> Optional[float]:
        """
        (Optional) Error on the reading value., _: °/s
        """
        return self.register(JD_GYROSCOPE_REG_ROTATION_RATES_ERROR).value()

    @property
    def max_rate(self) -> Optional[float]:
        """
        (Optional) Configures the range of rotation rates.
        The value will be "rounded up" to one of `max_rates_supported`., _: °/s
        """
        return self.register(JD_GYROSCOPE_REG_MAX_RATE).value()

    @max_rate.setter
    def max_rate(self, value: float) -> None:
        self.register(JD_GYROSCOPE_REG_MAX_RATE).set_values(value)


    
