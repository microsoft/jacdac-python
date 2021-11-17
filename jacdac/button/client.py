from typing import Union
from jacdac.bus import EV_CHANGE, Bus, Client, EV_EVENT, RawRegisterClient
from jacdac.packet import JDPacket
from jacdac.util import unpack
from .constants import *


class ButtonClient(Client):
    _pressed = False
    _pressure: RawRegisterClient

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_BUTTON, role)
        self._pressure = self.add_register(JD_BUTTON_REG_PRESSURE, "I")
        self.on(EV_EVENT, self._on_event)

    @property
    def pressed(self) -> bool:
        # Indicates if the button is pressed
        return self._pressed

    @pressed.setter
    def pressed(self, value: bool):
        self._pressed = value

    @property
    def pressure(self) -> Union[float, None]:
        reg = self.register(JD_BUTTON_REG_PRESSURE)
        return reg.floatValue(0, 100)

    def _on_event(self, pkt: JDPacket):
        code = pkt.event_code
        if (code == JD_BUTTON_EV_UP):
            self.pressed = False
        elif (code == JD_BUTTON_EV_DOWN or code == JD_BUTTON_EV_HOLD):
            self.pressed = True
