# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class MotionClient(Client):
    """
    A sensor, typically PIR, that detects object motion within a certain range
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_MOTION, JD_MOTION_PACK_FORMATS, role)
    

    @property
    def moving(self) -> Optional[bool]:
        """
        Reports is movement is currently detected by the sensor., 
        """
        reg = self.register(JD_MOTION_REG_MOVING)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @property
    def max_distance(self) -> Optional[float]:
        """
        (Optional) Maximum distance where objects can be detected., _: m
        """
        reg = self.register(JD_MOTION_REG_MAX_DISTANCE)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def angle(self) -> Optional[int]:
        """
        (Optional) Opening of the field of view, _: °
        """
        reg = self.register(JD_MOTION_REG_ANGLE)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @property
    def variant(self) -> Optional[MotionVariant]:
        """
        (Optional) Type of physical sensor, 
        """
        reg = self.register(JD_MOTION_REG_VARIANT)
        values = reg.values()
        return cast(Optional[MotionVariant], values[0] if values else None)

    def on_movement(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        A movement was detected.
        """
        return self.on_event(JD_MOTION_EV_MOVEMENT, handler)

    
