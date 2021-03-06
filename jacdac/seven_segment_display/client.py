# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional


class SevenSegmentDisplayClient(Client):
    """
    A 7-segment numeric display, with one or more digits.
    Implements a client for the `7-segment display <https://microsoft.github.io/jacdac-docs/services/sevensegmentdisplay>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SEVEN_SEGMENT_DISPLAY, JD_SEVEN_SEGMENT_DISPLAY_PACK_FORMATS, role)


    @property
    def digits(self) -> Optional[bytes]:
        """
        Each byte encodes the display status of a digit using,
        where lowest bit 0 encodes segment `A`, bit 1 encodes segments `B`, ..., bit 6 encodes segments `G`, and bit 7 encodes the decimal point (if present).
        If incoming `digits` data is smaller than `digit_count`, the remaining digits will be cleared.
        Thus, sending an empty `digits` payload clears the screen.
        
        ```text
        GFEDCBA DP
         - A -
         F   B
         |   |
         - G -
         |   |
         E   C   _
         |   |  |DP|
         - D -   -
        ```, 
        """
        return self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_DIGITS).value()

    @digits.setter
    def digits(self, value: bytes) -> None:
        self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_DIGITS).set_values(value)


    @property
    def brightness(self) -> Optional[float]:
        """
        (Optional) Controls the brightness of the LEDs. `0` means off., _: /
        """
        return self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_BRIGHTNESS).float_value(100)

    @brightness.setter
    def brightness(self, value: float) -> None:
        self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_BRIGHTNESS).set_values(value / 100)


    @property
    def double_dots(self) -> Optional[bool]:
        """
        (Optional) Turn on or off the column LEDs (separating minutes from hours, etc.) in of the segment.
        If the column LEDs is not supported, the value remains false., 
        """
        return self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_DOUBLE_DOTS).bool_value()

    @double_dots.setter
    def double_dots(self, value: bool) -> None:
        self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_DOUBLE_DOTS).set_values(value)


    @property
    def digit_count(self) -> Optional[int]:
        """
        The number of digits available on the display., 
        """
        return self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_DIGIT_COUNT).value()

    @property
    def decimal_point(self) -> Optional[bool]:
        """
        (Optional) True if decimal points are available (on all digits)., 
        """
        return self.register(JD_SEVEN_SEGMENT_DISPLAY_REG_DECIMAL_POINT).bool_value()


    def set_number(self, value: float) -> None:
        """
        Shows the number on the screen using the decimal dot if available.
        """
        # TODO: implement client command
        raise RuntimeError("client command not implemented")
    
