from jacdac.bus import Bus, Client
from jacdac.button.client_mixin import ButtonClientMixin
from .constants import *
from typing import Union
from jacdac.events import EventHandlerFn, UnsubscribeFn


class ButtonClient(Client, ButtonClientMixin):
    """
    A push-button, which returns to inactive position when not operated anymore.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_BUTTON, JD_BUTTON_PACK_FORMATS, role)
        self.init_mixin(self)

    @property
    def pressure(self) -> Union[float, None]:
        """
        Indicates the pressure state of the button, where ``0`` is open., /
        """
        reg = self.register(JD_BUTTON_REG_PRESSURE)
        return reg.value(0)

    @property
    def analog(self) -> Union[bool, None]:
        """
        (Optional) Indicates if the button provides analog ``pressure`` readings.
        """
        reg = self.register(JD_BUTTON_REG_ANALOG)
        return reg.value(0)

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
