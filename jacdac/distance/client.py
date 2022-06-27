# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class DistanceClient(SensorClient):
    """
    A sensor that determines the distance of an object without any physical contact involved.
    Implements a client for the `Distance <https://microsoft.github.io/jacdac-docs/services/distance>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_distance_value: Optional[float] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_DISTANCE, JD_DISTANCE_PACK_FORMATS, role)
        self.missing_distance_value = missing_distance_value

    @property
    def distance(self) -> Optional[float]:
        """
        Current distance from the object, _: m
        """
        self.refresh_reading()
        return self.register(JD_DISTANCE_REG_DISTANCE).value(self.missing_distance_value)

    @property
    def distance_error(self) -> Optional[float]:
        """
        (Optional) Absolute error on the reading value., _: m
        """
        return self.register(JD_DISTANCE_REG_DISTANCE_ERROR).value()

    @property
    def min_range(self) -> Optional[float]:
        """
        (Optional) Minimum measurable distance, _: m
        """
        return self.register(JD_DISTANCE_REG_MIN_RANGE).value()

    @property
    def max_range(self) -> Optional[float]:
        """
        (Optional) Maximum measurable distance, _: m
        """
        return self.register(JD_DISTANCE_REG_MAX_RANGE).value()

    @property
    def variant(self) -> Optional[DistanceVariant]:
        """
        (Optional) Determines the type of sensor used., 
        """
        return self.register(JD_DISTANCE_REG_VARIANT).value()

    
