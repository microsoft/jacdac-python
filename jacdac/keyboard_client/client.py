# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client, EventHandlerFn, UnsubscribeFn
from .constants import *



class KeyboardClientClient(Client):
    """
    Measures KeyboardClient.
    Implements a client for the `Keyboard client <https://microsoft.github.io/jacdac-docs/services/keyboardclient>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_KEYBOARD_CLIENT, JD_KEYBOARD_CLIENT_PACK_FORMATS, role)


    def on_down(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when a key is pressed.
        """
        return self.on_event(JD_KEYBOARD_CLIENT_EV_DOWN, handler)

    def on_hold(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when a key is held.
        """
        return self.on_event(JD_KEYBOARD_CLIENT_EV_HOLD, handler)

    
