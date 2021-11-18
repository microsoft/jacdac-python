# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *

from jacdac.events import EventHandlerFn, UnsubscribeFn

class CodalMessageBusClient(Client):
    """
    A service that uses the [CODAL message bus](https://lancaster-university.github.io/microbit-docs/ubit/messageBus/) to send and receive small messages.
     * 
     * You can find known values for `source` in [CODAL repository](https://github.com/lancaster-university/codal-core/blob/master/inc/core/CodalComponent.h)
     * In MakeCode, you can listen for custom `source`, `value` values using [control.onEvent](https://makecode.microbit.org/reference/control/on-event].
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_CODAL_MESSAGE_BUS, JD_CODAL_MESSAGE_BUS_PACK_FORMATS, role)
    

    def on_message(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Raised by the server is triggered by the server. The filtering logic of which event to send over JACDAC is up to the server implementation.
        """
        return self.on_event(JD_CODAL_MESSAGE_BUS_EV_MESSAGE, handler)


    def send(self, source: int, value: int) -> None:
        """
        Send a message on the CODAL bus. If `source` is `0`, it is treated as wildcard.
        """
        self.send_cmd_packed(JD_CODAL_MESSAGE_BUS_CMD_SEND, source, value)
    
