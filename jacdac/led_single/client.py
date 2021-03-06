# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, Tuple


class LedSingleClient(Client):
    """
    A controller for 1 or more monochrome or RGB LEDs connected in parallel.
    Implements a client for the `LED Single <https://microsoft.github.io/jacdac-docs/services/ledsingle>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_LED_SINGLE, JD_LED_SINGLE_PACK_FORMATS, role)


    @property
    def color(self) -> Optional[Tuple[int, int, int]]:
        """
        The current color of the LED., 
        """
        return self.register(JD_LED_SINGLE_REG_COLOR).value()

    @property
    def max_power(self) -> Optional[int]:
        """
        (Optional) Limit the power drawn by the light-strip (and controller)., _: mA
        """
        return self.register(JD_LED_SINGLE_REG_MAX_POWER).value()

    @max_power.setter
    def max_power(self, value: int) -> None:
        self.register(JD_LED_SINGLE_REG_MAX_POWER).set_values(value)


    @property
    def led_count(self) -> Optional[int]:
        """
        (Optional) If known, specifies the number of LEDs in parallel on this device., 
        """
        return self.register(JD_LED_SINGLE_REG_LED_COUNT).value()

    @property
    def wave_length(self) -> Optional[int]:
        """
        (Optional) If monochrome LED, specifies the wave length of the LED., _: nm
        """
        return self.register(JD_LED_SINGLE_REG_WAVE_LENGTH).value()

    @property
    def luminous_intensity(self) -> Optional[int]:
        """
        (Optional) The luminous intensity of the LED, at full value, in micro candella., _: mcd
        """
        return self.register(JD_LED_SINGLE_REG_LUMINOUS_INTENSITY).value()

    @property
    def variant(self) -> Optional[LedSingleVariant]:
        """
        (Optional) The physical type of LED., 
        """
        return self.register(JD_LED_SINGLE_REG_VARIANT).value()


    def animate(self, to_red: int, to_green: int, to_blue: int, speed: int) -> None:
        """
        This has the same semantics as `set_status_light` in the control service.
        """
        self.send_cmd_packed(JD_LED_SINGLE_CMD_ANIMATE, to_red, to_green, to_blue, speed)
    
