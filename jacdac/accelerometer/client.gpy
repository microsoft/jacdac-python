from jacdac.bus import Bus, Client
from .constants import *
from typing import Union
from jacdac.events import HandlerFn

class AccelerometerClient(Client):
    """
    A 3-axis accelerometer.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_ACCELEROMETER, JD_ACCELEROMETER_PACK_FORMATS, role)
    

    @property
    def x(self) -> Union[float, None]:
        """
        Indicates the current forces acting on accelerometer., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_FORCES)
        return reg.value(0)

    @property
    def y(self) -> Union[float, None]:
        """
        Indicates the current forces acting on accelerometer., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_FORCES)
        return reg.value(1)

    @property
    def z(self) -> Union[float, None]:
        """
        Indicates the current forces acting on accelerometer., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_FORCES)
        return reg.value(2)

    @property
    def forces_error(self) -> Union[float, None]:
        """
        (Optional) Error on the reading value., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_FORCES_ERROR)
        return reg.value(0)

    @property
    def max_force(self) -> Union[float, None]:
        """
        (Optional) Configures the range forces detected.
        The value will be "rounded up" to one of `max_forces_supported`., g
        """
        reg = self.register(JD_ACCELEROMETER_REG_MAX_FORCE)
        return reg.value(0)

    @max_force.setter
    def max_force(self, value: float) -> None:
        reg = self.register(JD_ACCELEROMETER_REG_MAX_FORCE)
        reg.set_value(0, value)


    def on_tilt_up(self, handler: HandlerFn) -> None:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        # TODO

    def on_tilt_down(self, handler: HandlerFn) -> None:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        # TODO

    def on_tilt_left(self, handler: HandlerFn) -> None:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        # TODO

    def on_tilt_right(self, handler: HandlerFn) -> None:
        """
        Emitted when accelerometer is tilted in the given direction.
        """
        # TODO

    def on_face_up(self, handler: HandlerFn) -> None:
        """
        Emitted when accelerometer is laying flat in the given direction.
        """
        # TODO

    def on_face_down(self, handler: HandlerFn) -> None:
        """
        Emitted when accelerometer is laying flat in the given direction.
        """
        # TODO

    def on_freefall(self, handler: HandlerFn) -> None:
        """
        Emitted when total force acting on accelerometer is much less than 1g.
        """
        # TODO

    def on_shake(self, handler: HandlerFn) -> None:
        """
        Emitted when forces change violently a few times.
        """
        # TODO

    def on_force_2g(self, handler: HandlerFn) -> None:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        # TODO

    def on_force_3g(self, handler: HandlerFn) -> None:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        # TODO

    def on_force_6g(self, handler: HandlerFn) -> None:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        # TODO

    def on_force_8g(self, handler: HandlerFn) -> None:
        """
        Emitted when force in any direction exceeds given threshold.
        """
        # TODO

    
