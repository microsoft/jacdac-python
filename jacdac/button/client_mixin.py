from typing import Union
from jacdac.bus import Client, EV_EVENT
from jacdac.button.constants import JD_BUTTON_EV_DOWN, JD_BUTTON_EV_HOLD, JD_BUTTON_EV_UP
from jacdac.packet import JDPacket


class ButtonClientMixin:
    _pressed = False

    def init_mixin(self, client: Client) -> None:
        self.client = client
        self.client.on(EV_EVENT, self._on_event)

    @property
    def pressed(self) -> Union[bool, None]:
        """
        Determines if the button is pressed currently.

        If the event ``down`` is observed, ``pressed`` is true; if ``up`` or ``hold`` are observed, ``pressed`` is false.
        To initialize, wait for any event or timeout to ``pressed`` is true after 750ms (1.5x hold time).
        """
        return self._pressed

    @pressed.setter
    def pressed(self, value: bool):
        self._pressed = value

    def _on_event(self, pkt: JDPacket):
        code = pkt.event_code
        if (code == JD_BUTTON_EV_UP):
            self.pressed = False
        elif (code == JD_BUTTON_EV_DOWN):
            self.pressed = True
        elif code == JD_BUTTON_EV_HOLD:
            self.pressed = True
