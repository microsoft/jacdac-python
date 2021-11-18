from jacdac.bus import Bus, EV_EVENT
from jacdac.button.constants import JD_BUTTON_EV_DOWN, JD_BUTTON_EV_HOLD, JD_BUTTON_EV_UP
from jacdac.packet import JDPacket
from .client_base import ButtonClientBase


class ButtonClient(ButtonClientBase):
    """A push-button, which returns to inactive position when not operated anymore."""

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, role)
        self.on(EV_EVENT, self._on_event)
        self._pressed = False

    @property
    def pressed(self) -> bool:
        """
        Determines if the button is pressed currently.

        If the event ``down`` is observed, ``pressed`` is true; if ``up`` or ``hold`` are observed, ``pressed`` is false.
        To initialize, wait for any event or timeout to ``pressed`` is true after 750ms (1.5x hold time).
        """
        return self._pressed

    def _on_event(self, pkt: JDPacket):
        code = pkt.event_code
        if (code == JD_BUTTON_EV_UP):
            self._pressed = False
        elif (code == JD_BUTTON_EV_DOWN):
            self._pressed = True
        elif code == JD_BUTTON_EV_HOLD:
            self._pressed = True
