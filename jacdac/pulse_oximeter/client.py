# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class PulseOximeterClient(Client):
    """
    A sensor approximating the oxygen level. 
     * 
     * **Jacdac is not suitable for medical devices and should NOT be used in any kind of device to diagnose or treat any medical conditions.**
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_PULSE_OXIMETER, JD_PULSE_OXIMETER_PACK_FORMATS, role)
    

    @property
    def oxygen(self) -> Optional[float]:
        """
        The estimated oxygen level in blood., _: %
        """
        reg = self.register(JD_PULSE_OXIMETER_REG_OXYGEN)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def oxygen_error(self) -> Optional[float]:
        """
        (Optional) The estimated error on the reported sensor data., _: %
        """
        reg = self.register(JD_PULSE_OXIMETER_REG_OXYGEN_ERROR)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    
