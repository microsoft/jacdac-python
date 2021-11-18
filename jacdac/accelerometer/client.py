from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, Union, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class AccelerometerClient(Client):
    """
    A 3-axis accelerometer.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_ACCELEROMETER, JD_ACCELEROMETER_PACK_FORMATS, role)
    

    @property
    def forces(self) -> Optional[tuple[float,float,float]]:
        """
        Indicates the current forces acting on accelerometer., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_FORCES)
        values = reg.unpacked()
        return values

    @property
    def forces_error(self) -> Union[float, None]:
        """
        (Optional) Error on the reading value., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_FORCES_ERROR)
        value = reg.value(0)
        return cast(Union[float, None], value)

    @property
    def max_force(self) -> Union[float, None]:
        """
        (Optional) Configures the range forces detected.
        The value will be "rounded up" to one of `max_forces_supported`., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_MAX_FORCE)
        value = reg.value(0)
        return cast(Union[float, None], value)

    @max_force.setter
    def max_force(self, value: float) -> None:
        reg = self.register(JD_ACCELEROMETER_REG_MAX_FORCE)
        reg.set_value(0, value)


    def on_tilt_up(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        return self.on_event(JD_ACCELEROMETER_EV_TILT_UP, handler)

    def on_tilt_down(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        return self.on_event(JD_ACCELEROMETER_EV_TILT_DOWN, handler)

    def on_tilt_left(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        return self.on_event(JD_ACCELEROMETER_EV_TILT_LEFT, handler)

    def on_tilt_right(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        return self.on_event(JD_ACCELEROMETER_EV_TILT_RIGHT, handler)

    def on_face_up(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when accelerometer is laying flat in the given direction.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FACE_UP, handler)

    def on_face_down(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when accelerometer is laying flat in the given direction.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FACE_DOWN, handler)

    def on_freefall(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when total force acting on accelerometer is much less than 1g.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FREEFALL, handler)

    def on_shake(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when forces change violently a few times.
        """
        return self.on_event(JD_ACCELEROMETER_EV_SHAKE, handler)

    def on_force_2g(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FORCE_2G, handler)

    def on_force_3g(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FORCE_3G, handler)

    def on_force_6g(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FORCE_6G, handler)

    def on_force_8g(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        return self.on_event(JD_ACCELEROMETER_EV_FORCE_8G, handler)

    
