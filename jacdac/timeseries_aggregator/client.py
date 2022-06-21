# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional


class TimeseriesAggregatorClient(Client):
    """
    Supports aggregating timeseries data (especially sensor readings)
     * and sending them to a cloud/storage service.
     * Used in Jacscript.
     * 
     * Note that `f64` values are not necessarily aligned.
    Implements a client for the `Timeseries Aggregator <https://microsoft.github.io/jacdac-docs/services/timeseriesaggregator>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_TIMESERIES_AGGREGATOR, JD_TIMESERIES_AGGREGATOR_PACK_FORMATS, role)


    @property
    def now(self) -> Optional[int]:
        """
        This can queried to establish local time on the device., _: us
        """
        return self.register(JD_TIMESERIES_AGGREGATOR_REG_NOW).value()

    @property
    def fast_start(self) -> Optional[bool]:
        """
        When `true`, the windows will be shorter after service reset and gradually extend to requested length.
        This is ensure valid data is being streamed in program development., 
        """
        return self.register(JD_TIMESERIES_AGGREGATOR_REG_FAST_START).bool_value()

    @fast_start.setter
    def fast_start(self, value: bool) -> None:
        self.register(JD_TIMESERIES_AGGREGATOR_REG_FAST_START).set_values(value)


    @property
    def default_window(self) -> Optional[int]:
        """
        Window for timeseries for which `set_window` was never called.
        Note that windows returned initially may be shorter if `fast_start` is enabled., _: ms
        """
        return self.register(JD_TIMESERIES_AGGREGATOR_REG_DEFAULT_WINDOW).value()

    @default_window.setter
    def default_window(self, value: int) -> None:
        self.register(JD_TIMESERIES_AGGREGATOR_REG_DEFAULT_WINDOW).set_values(value)


    @property
    def default_upload(self) -> Optional[bool]:
        """
        Whether labelled timeseries for which `set_upload` was never called should be automatically uploaded., 
        """
        return self.register(JD_TIMESERIES_AGGREGATOR_REG_DEFAULT_UPLOAD).bool_value()

    @default_upload.setter
    def default_upload(self, value: bool) -> None:
        self.register(JD_TIMESERIES_AGGREGATOR_REG_DEFAULT_UPLOAD).set_values(value)


    @property
    def upload_unlabelled(self) -> Optional[bool]:
        """
        Whether automatically created timeseries not bound in role manager should be uploaded., 
        """
        return self.register(JD_TIMESERIES_AGGREGATOR_REG_UPLOAD_UNLABELLED).bool_value()

    @upload_unlabelled.setter
    def upload_unlabelled(self, value: bool) -> None:
        self.register(JD_TIMESERIES_AGGREGATOR_REG_UPLOAD_UNLABELLED).set_values(value)


    @property
    def sensor_watchdog_period(self) -> Optional[int]:
        """
        If no data is received from any sensor within given period, the device is rebooted.
        Set to `0` to disable (default).
        Updating user-provided timeseries does not reset the watchdog., _: ms
        """
        return self.register(JD_TIMESERIES_AGGREGATOR_REG_SENSOR_WATCHDOG_PERIOD).value()

    @sensor_watchdog_period.setter
    def sensor_watchdog_period(self, value: int) -> None:
        self.register(JD_TIMESERIES_AGGREGATOR_REG_SENSOR_WATCHDOG_PERIOD).set_values(value)



    def clear(self, ) -> None:
        """
        Remove all pending timeseries.
        """
        self.send_cmd_packed(JD_TIMESERIES_AGGREGATOR_CMD_CLEAR, )

    def update(self, value: float, label: str) -> None:
        """
        Add a data point to a timeseries.
        """
        self.send_cmd_packed(JD_TIMESERIES_AGGREGATOR_CMD_UPDATE, value, label)

    def set_window(self, duration: int, label: str) -> None:
        """
        Set aggregation window.
        Setting to `0` will restore default.
        """
        self.send_cmd_packed(JD_TIMESERIES_AGGREGATOR_CMD_SET_WINDOW, duration, label)

    def set_upload(self, upload: bool, label: str) -> None:
        """
        Set whether or not the timeseries will be uploaded to the cloud.
        The `stored` reports are generated regardless.
        """
        self.send_cmd_packed(JD_TIMESERIES_AGGREGATOR_CMD_SET_UPLOAD, upload, label)
    