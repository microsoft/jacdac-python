# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class LightBulbClient(Client):
    """
    A light bulb controller.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_LIGHT_BULB, JD_LIGHT_BULB_PACK_FORMATS, role)
    

    @property
    def brightness(self) -> Optional[float]:
        """
        Indicates the brightness of the light bulb. Zero means completely off and 0xffff means completely on.
        For non-dimmeable lights, the value should be clamp to 0xffff for any non-zero value., _: /
        """
        reg = self.register(JD_LIGHT_BULB_REG_BRIGHTNESS)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @brightness.setter
    def brightness(self, value: float) -> None:
        reg = self.register(JD_LIGHT_BULB_REG_BRIGHTNESS)
        reg.set_values(value) # type: ignore


    @property
    def dimmeable(self) -> Optional[bool]:
        """
        (Optional) Indicates if the light supports dimming., 
        """
        reg = self.register(JD_LIGHT_BULB_REG_DIMMEABLE)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    def on_on(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when the light brightness is greater than 0.
        """
        return self.on_event(JD_LIGHT_BULB_EV_ON, handler)

    def on_off(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when the light is completely off with brightness to 0.
        """
        return self.on_event(JD_LIGHT_BULB_EV_OFF, handler)

    
