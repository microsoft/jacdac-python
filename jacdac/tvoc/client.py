# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class TvocClient(SensorClient):
    """
    Measures equivalent Total Volatile Organic Compound levels.
    Implements a client for the `Total Volatile organic compound <https://microsoft.github.io/jacdac-docs/services/tvoc>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_TVOC_value: Optional[float] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_TVOC, JD_TVOC_PACK_FORMATS, role)
        self.missing_TVOC_value = missing_TVOC_value

    @property
    def TVOC(self) -> Optional[float]:
        """
        Total volatile organic compound readings in parts per billion., _: ppb
        """
        self.refresh_reading()
        return self.register(JD_TVOC_REG_TVOC).value(self.missing_TVOC_value)

    @property
    def TVOC_error(self) -> Optional[float]:
        """
        (Optional) Error on the reading data, _: ppb
        """
        return self.register(JD_TVOC_REG_TVOC_ERROR).value()

    @property
    def min_TVOC(self) -> Optional[float]:
        """
        Minimum measurable value, _: ppb
        """
        return self.register(JD_TVOC_REG_MIN_TVOC).value()

    @property
    def max_TVOC(self) -> Optional[float]:
        """
        Minimum measurable value., _: ppb
        """
        return self.register(JD_TVOC_REG_MAX_TVOC).value()

    
