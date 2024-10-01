# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional


class GPIOClient(SensorClient):
    """
    Access to General Purpose Input/Output (GPIO) pins on a board.
     * The pins are indexed `0 ... num_pins-1`.
     * The indexing does not correspond to hardware pin names, nor labels on the board (see `get_pin_info` command for that),
     * and should **not** be exposed to the user.
    Implements a client for the `GPIO <https://microsoft.github.io/jacdac-docs/services/gpio>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_state_value: Optional[bytes] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_GPIO, JD_GPIO_PACK_FORMATS, role)
        self.missing_state_value = missing_state_value

    @property
    def state(self) -> Optional[bytes]:
        """
        For every pin set to `Input*` the corresponding **bit** in `digital_values` will be `1` if and only if
        the pin is high.
        For other pins, the bit is `0`.
        This is normally streamed at low-ish speed, but it's also automatically reported whenever
        a digital input pin changes value (throttled to ~100Hz).
        The analog values can be read with the `ADC` service., 
        """
        self.refresh_reading()
        return self.register(JD_GPIO_REG_STATE).value(self.missing_state_value)

    @property
    def num_pins(self) -> Optional[int]:
        """
        Number of pins that can be operated through this service., _: #
        """
        return self.register(JD_GPIO_REG_NUM_PINS).value()


    def pin_info(self, pin: int) -> None:
        """
        Report capabilities and name of a pin.
        """
        self.send_cmd_packed(JD_GPIO_CMD_PIN_INFO, pin)

    def pin_by_label(self, label: str) -> None:
        """
        This responds with `pin_info` report.
        """
        self.send_cmd_packed(JD_GPIO_CMD_PIN_BY_LABEL, label)

    def pin_by_hw_pin(self, hw_pin: int) -> None:
        """
        This responds with `pin_info` report.
        """
        self.send_cmd_packed(JD_GPIO_CMD_PIN_BY_HW_PIN, hw_pin)
    