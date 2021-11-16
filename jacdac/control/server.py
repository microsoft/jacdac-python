import time
import sys
from .constants import *
from jacdac.bus import Server, Bus, EV_IDENTIFY
from jacdac.util import pack, logv
from jacdac.packet import JDPacket


class ControlServer(Server):
    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_CONTROL)
        self.restart_counter = 0

    def queue_announce(self):
        logv("announce: %d " % self.restart_counter)
        self.restart_counter += 1
        ids = [s.service_class for s in self.bus. servers]
        rest = self.restart_counter
        if rest > 0xf:
            rest = 0xf
        ids[0] = (
            rest |
            JD_CONTROL_ANNOUNCE_FLAGS_IS_CLIENT |
            JD_CONTROL_ANNOUNCE_FLAGS_SUPPORTS_ACK |
            JD_CONTROL_ANNOUNCE_FLAGS_SUPPORTS_BROADCAST |
            JD_CONTROL_ANNOUNCE_FLAGS_SUPPORTS_FRAMES
        )
        buf = pack("%dI" % len(ids), ids)
        self.send_report(JDPacket(cmd=0, data=buf))

        # auto bind
        # if jacdac.role_manager_server.auto_bind:
        #     self.auto_bind_cnt++
        #     # also, only do it every two announces (TBD)
        #     if self.auto_bind_cnt >= 2:
        #         self.auto_bind_cnt = 0
        #         jacdac.role_manager_server.bind_roles()

    # def handle_flood_ping(self, pkt: JDPacket):
    #     num_responses, counter, size = pkt.unpack("IIB")
    #     payload = bytearray(4 + size)
    #     for i in range(size): payload[4+i]=i
    #     def queue_ping():
    #         if num_responses <= 0:
    #             control.internal_on_event(
    #                 jacdac.__physId(),
    #                 EVT_TX_EMPTY,
    #                 do_nothing
    #             )
    #         else:
    #             payload.set_number(NumberFormat.UInt32LE, 0, counter)
    #             self.send_report(
    #                 JDPacket.from(ControlCmd.FloodPing, payload)
    #             )
    #             num_responses--
    #             counter++
    #     control.internal_on_event(jacdac.__physId(), EVT_TX_EMPTY, queue_ping)
    #     queue_ping()

    def handle_packet(self, pkt: JDPacket):
        if pkt.is_reg_get:
            if pkt.reg_code == JD_CONTROL_REG_UPTIME:
                self.send_report(JDPacket.packed(
                    JD_GET(JD_CONTROL_REG_UPTIME), "Q",  time.monotonic_ns() // 1000))
        else:
            cmd = pkt.service_command
            if cmd == JD_CONTROL_CMD_SERVICES:
                self.queue_announce()
            elif cmd == JD_CONTROL_CMD_IDENTIFY:
                self.log("identify")
                self.bus.emit(EV_IDENTIFY)
            elif cmd == JD_CONTROL_CMD_RESET:
                sys.exit()  # TODO?
