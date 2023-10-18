# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient
from .constants import *
from typing import Optional, Tuple


class RealTimeClockClient(SensorClient):
    """
    Real time clock to support collecting data with precise time stamps.
    Implements a client for the `Real time clock <https://microsoft.github.io/jacdac-docs/services/realtimeclock>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_local_time_value: Optional[Tuple[int, int, int, int, int, int, int]] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_REAL_TIME_CLOCK, JD_REAL_TIME_CLOCK_PACK_FORMATS, role, preferred_interval = 1000)
        self.missing_local_time_value = missing_local_time_value

    @property
    def local_time(self) -> Optional[Tuple[int, int, int, int, int, int, int]]:
        """
        Current time in 24h representation. Default streaming period is 1 second.
        
        -   `day_of_month` is day of the month, starting at `1`
        -   `day_of_week` is day of the week, starting at `1` as monday. Leave at 0 if unsupported., 
        """
        self.refresh_reading()
        return self.register(JD_REAL_TIME_CLOCK_REG_LOCAL_TIME).value(self.missing_local_time_value)

    @property
    def drift(self) -> Optional[float]:
        """
        (Optional) Time drift since the last call to the `set_time` command., _: s
        """
        return self.register(JD_REAL_TIME_CLOCK_REG_DRIFT).value()

    @property
    def precision(self) -> Optional[float]:
        """
        (Optional) Error on the clock, in parts per million of seconds., _: ppm
        """
        return self.register(JD_REAL_TIME_CLOCK_REG_PRECISION).value()

    @property
    def variant(self) -> Optional[RealTimeClockVariant]:
        """
        (Optional) The type of physical clock used by the sensor., 
        """
        return self.register(JD_REAL_TIME_CLOCK_REG_VARIANT).value()


    def set_time(self, year: int, month: int, day_of_month: int, day_of_week: int, hour: int, min: int, sec: int) -> None:
        """
        Sets the current time and resets the error.
        """
        self.send_cmd_packed(JD_REAL_TIME_CLOCK_CMD_SET_TIME, year, month, day_of_month, day_of_week, hour, min, sec)
    
