# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class PressureButtonClient(Client):
    """
    A pressure sensitive push-button.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_PRESSURE_BUTTON, JD_PRESSURE_BUTTON_PACK_FORMATS, role)
    

    @property
    def threshold(self) -> Optional[float]:
        """
        Indicates the threshold for ``up`` events., _: /
        """
        reg = self.register(JD_PRESSURE_BUTTON_REG_THRESHOLD)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @threshold.setter
    def threshold(self, value: float) -> None:
        reg = self.register(JD_PRESSURE_BUTTON_REG_THRESHOLD)
        reg.set_values(value)


    