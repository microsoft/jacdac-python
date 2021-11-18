from jacdac.bus import Bus, Client
from .constants import *
from typing import Union, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class RelayClient(Client):
    """
    A switching relay.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_RELAY, JD_RELAY_PACK_FORMATS, role)
    

    @property
    def closed(self) -> Union[bool, None]:
        """
        Indicates whether the relay circuit is currently energized (closed) or not.
        """
        reg = self.register(JD_RELAY_REG_CLOSED)
        value = reg.value(0)
        return cast(Union[bool, None], value)

    @closed.setter
    def closed(self, value: bool) -> None:
        reg = self.register(JD_RELAY_REG_CLOSED)
        reg.set_value(0, value)


    @property
    def variant(self) -> Union[RelayVariant, None]:
        """
        (Optional) Describes the type of relay used.
        """
        reg = self.register(JD_RELAY_REG_VARIANT)
        value = reg.value(0)
        return cast(Union[RelayVariant, None], value)

    @property
    def max_switching_current(self) -> Union[int, None]:
        """
        (Optional) Maximum switching current for a resistive load., mA
        """
        reg = self.register(JD_RELAY_REG_MAX_SWITCHING_CURRENT)
        value = reg.value(0)
        return cast(Union[int, None], value)

    def on_active(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when relay goes from `inactive` to `active` state.
        Normally open (NO) relays close the circuit when activated.
        """
        return self.on_event(JD_RELAY_EV_ACTIVE, handler)

    def on_inactive(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when relay goes from `active` to `inactive` state.
        Normally closed (NC) relays open the circuit when activated.
        """
        return self.on_event(JD_RELAY_EV_INACTIVE, handler)

    
