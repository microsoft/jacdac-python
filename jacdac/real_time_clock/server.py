from ..bus import SensorServer, Bus
from ..packet import JDPacket
from .constants import *
from time import localtime


class RealTimeClockServer(SensorServer):
    """A server for the real time clock service using Python time."""

    def __init__(self, bus: Bus, *, instance_name: str = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_REAL_TIME_CLOCK,
                         instance_name=instance_name,
                         streaming_interval=1000,
                         streaming_preferred_interval=1000)

    def send_reading(self):
        t = localtime()
        fmt = JD_REAL_TIME_CLOCK_PACK_FORMATS[JD_REAL_TIME_CLOCK_REG_LOCAL_TIME]
        self.send_report(JDPacket.packed(
            JD_GET(JD_REAL_TIME_CLOCK_REG_LOCAL_TIME), fmt, t.tm_year, t.tm_mon, t.tm_mday, t.tm_wday, t.tm_hour, t.tm_min, t.tm_sec))

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command
        if cmd == JD_GET(JD_REAL_TIME_CLOCK_REG_LOCAL_TIME):
            self.send_reading()
        elif cmd == JD_GET(JD_REAL_TIME_CLOCK_REG_VARIANT):
            fmt = JD_REAL_TIME_CLOCK_PACK_FORMATS[JD_REAL_TIME_CLOCK_REG_VARIANT]
            self.send_report(JDPacket.packed(
                cmd, fmt, RealTimeClockVariant.COMPUTER))
        elif cmd == JD_GET(JD_REAL_TIME_CLOCK_REG_DRIFT):
            self.send_report(pkt.not_implemented())
        else:
            super().handle_packet(pkt)
