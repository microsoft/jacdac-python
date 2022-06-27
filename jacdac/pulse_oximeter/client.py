# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class PulseOximeterClient(SensorClient):
    """
    A sensor approximating the oxygen level.
     * 
     * **Jacdac is not suitable for medical devices and should NOT be used in any kind of device to diagnose or treat any medical conditions.**
    Implements a client for the `Pulse Oximeter <https://microsoft.github.io/jacdac-docs/services/pulseoximeter>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_oxygen_value: Optional[float] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_PULSE_OXIMETER, JD_PULSE_OXIMETER_PACK_FORMATS, role)
        self.missing_oxygen_value = missing_oxygen_value

    @property
    def oxygen(self) -> Optional[float]:
        """
        The estimated oxygen level in blood., _: %
        """
        self.refresh_reading()
        return self.register(JD_PULSE_OXIMETER_REG_OXYGEN).value(self.missing_oxygen_value)

    @property
    def oxygen_error(self) -> Optional[float]:
        """
        (Optional) The estimated error on the reported sensor data., _: %
        """
        return self.register(JD_PULSE_OXIMETER_REG_OXYGEN_ERROR).value()

    
