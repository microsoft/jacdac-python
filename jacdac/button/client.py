from typing import Union
from jacdac.bus import Bus, Client, EV_EVENT, EventHandlerFn
from jacdac.packet import JDPacket
from .constants import JD_SERVICE_CLASS_BUTTON, JD_BUTTON_PACK_FORMATS, JD_BUTTON_REG_PRESSURE, JD_BUTTON_EV_UP, JD_BUTTON_EV_DOWN, JD_BUTTON_EV_HOLD
from jacdac.events import UnsubscribeFn


class PressedMixin:
    _pressed = False

    def init_pressed(self, client: Client) -> None:
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


class ButtonClient(Client, PressedMixin):

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_BUTTON, JD_BUTTON_PACK_FORMATS, role)
        self.init_pressed(self)

    @property
    def pressure(self) -> Union[float, None]:
        reg = self.register(JD_BUTTON_REG_PRESSURE)
        return reg.float_value(0, 100)

    def on_down(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when button goes from inactive to active.
        """
        return self.on_event(JD_BUTTON_EV_DOWN, handler)

    def on_up(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when button goes from active to inactive. The 'time' parameter 
        records the amount of time between the down and up events.
        """
        return self.on_event(JD_BUTTON_EV_UP, handler)

    def on_hold(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when the press time is greater than 500ms, and then at least every 500ms 
        as long as the button remains pressed. The 'time' parameter records the the amount of time
        that the button has been held (since the down event).
        """
        return self.on_event(JD_BUTTON_EV_HOLD, handler)
