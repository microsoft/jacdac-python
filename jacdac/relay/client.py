from jacdac.bus import Bus, Client
from .constants import *
from typing import Union
from jacdac.events import HandlerFn

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
        return reg.value(0)

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
        return reg.value(0)

    @property
    def max_switching_current(self) -> Union[float, None]:
        """
        (Optional) Maximum switching current for a resistive load., mA
        """
        reg = self.register(JD_RELAY_REG_MAX_SWITCHING_CURRENT)
        return reg.value(0)

    def on_active(self, handler: HandlerFn) -> None:
        """
        Emitted when relay goes from `inactive` to `active` state.
        Normally open (NO) relays close the circuit when activated.
        """
        # TODO

    def on_inactive(self, handler: HandlerFn) -> None:
        """
        Emitted when relay goes from `active` to `inactive` state.
        Normally closed (NC) relays open the circuit when activated.
        """
        # TODO

    
