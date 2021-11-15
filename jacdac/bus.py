import threading
import random
from typing import Optional, TypeVar, Union, cast

from .jdconstants import *
from .events import *
from .packet import *
from .transport import Transport
from .taskq import TaskQ

import jacdac.util as util
from .util import now


EV_CHANGE = "change"
EV_DEVICE_CONNECT = "deviceConnect"
EV_DEVICE_CHANGE = "deviceChange"
EV_DEVICE_ANNOUNCE = "deviceAnnounce"
EV_SELF_ANNOUNCE = "selfAnnounce"
EV_PACKET_PROCESS = "packetProcess"
EV_REPORT_RECEIVE = "reportReceive"
EV_REPORT_UPDATE = "reportUpdate"
EV_RESTART = "restart"
EV_PACKET_RECEIVE = "packetReceive"
EV_EVENT = "packetEvent"
EV_STATUS_EVENT = "statusEvent"
EV_IDENTIFY = "identify"
EV_CONNECTED = "connected"
EV_DISCONNECTED = "disconnected"

_ACK_RETRIES = const(4)
_ACK_DELAY = const(40)

RegType = TypeVar('RegType', bound=Union[int, tuple[int, ...]])


def _service_matches(dev: 'Device', serv: bytearray):
    ds = dev.services
    if not ds or len(ds) != len(serv):
        return False
    for i in range(4, len(serv)):
        if ds[i] != serv[i]:
            return False
    return True


class Bus(EventEmitter):
    def __init__(self, transport: Transport, devid: str = None) -> None:
        super().__init__(self)
        self.devices: list['Device'] = []
        self.unattached_clients: list['Client'] = []
        self.all_clients: list['Client'] = []
        self.servers: list['Server'] = []
        self.taskq = TaskQ()
        if devid is None:
            devid = random.randbytes(8).hex()
        self.self_device = Device(self, devid, bytearray(4))
        self.process_thread = threading.Thread(target=self._process_task)
        self.transport = transport

        from . import ctrl
        ctrls = ctrl.CtrlServer(self)  # attach control server

        def announce():
            self.emit(EV_SELF_ANNOUNCE)
            self._gc_devices()
            ctrls.queue_announce()
        self.taskq.recurring(500, announce)

        # self.taskq.recurring(2000, self.debug_dump)

        self.process_thread.start()

        from . import sample
        sample.acc_sample(self)

    def _process_task(self):
        while True:
            self.taskq.execute()
            pkt = self.transport.receive(timeout_ms=self.taskq.sleeptime())
            if pkt:
                self.process_packet(JDPacket(frombytes=pkt))

    def debug_dump(self):
        print("Devices:")
        for dev in self.devices:
            info = dev.debug_info()
            if dev is self.self_device:
                info = "SELF: " + info
            print(info)
        print("END")

    def _gc_devices(self):
        now_ = now()
        cutoff = now_ - 2000
        self.self_device.last_seen = now_  # make sure not to gc self

        newdevs: list['Device'] = []
        for dev in self.devices:
            if dev.last_seen < cutoff:
                dev._destroy()
            else:
                newdevs.append(dev)
        if len(newdevs) != len(self.devices):
            self.devices = newdevs
            self.emit(EV_DEVICE_CHANGE)
            self.emit(EV_CHANGE)

    def _send_core(self, pkt: JDPacket):
        assert len(pkt._data) == pkt._header[12]
        self.transport.send(pkt._header + pkt._data)
        self.process_packet(pkt)  # handle loop-back packet

    def clear_attach_cache(self):
        pass

    def mk_event_cmd(self, ev_code: int):
        if not self._event_counter:
            self._event_counter = 0
        self._event_counter = (self._event_counter +
                               1) & CMD_EVENT_COUNTER_MASK
        assert (ev_code >> 8) == 0
        return (
            CMD_EVENT_MASK |
            (self._event_counter << CMD_EVENT_COUNTER_POS) |
            ev_code
        )

    def _reattach(self, dev: 'Device'):
        dev.last_seen = now()
        log("reattaching services to {}; {}/{} to attach", dev,
            len(self.unattached_clients), len(self.all_clients))
        new_clients: list['Client'] = []
        occupied = bytearray(dev.num_service_classes)
        for c in dev.clients:
            if c.broadcast:
                c._detach()
                continue  # will re-attach

            assert c.service_index is not None
            new_class = dev.service_class_at(c.service_index)
            if new_class == c.service_class and dev.matches_role_at(c.role, c.service_index):
                new_clients.append(c)
                occupied[c.service_index] = 1
            else:
                c._detach()

        dev.clients = new_clients
        self.emit(EV_DEVICE_ANNOUNCE, dev)

        if len(self.unattached_clients) == 0:
            return

        for i in range(1, dev.num_service_classes):
            if occupied[i]:
                continue
            service_class = dev.service_class_at(i)
            for cc in self.unattached_clients:
                if cc.service_class == service_class:
                    if cc._attach(dev, i):
                        break

    def process_packet(self, pkt: JDPacket):
        log("route: {}", pkt)
        dev_id = pkt.device_identifier
        multi_command_class = pkt.multicommand_class

        # TODO implement send queue for packet compression

        # if (pkt.requires_ack):
        #     pkt.requires_ack = False  # make sure we only do it once
        #     if pkt.device_identifier == self.self_device.device_id:
        #         ack = JDPacket(cmd=pkt.crc)
        #         ack.service_index = JD_SERVICE_INDEX_CRC_ACK
        #         ack._send_report(self.self_device)

        self.emit(EV_PACKET_PROCESS, pkt)

        if multi_command_class != None:
            if not pkt.is_command:
                return  # only commands supported in multi-command
            for h in self.servers:
                if h.service_class == multi_command_class:
                    # pretend it's directly addressed to us
                    pkt.device_identifier = self.self_device.device_id
                    pkt.service_index = h.service_index
                    h.handle_packet_outer(pkt)
        elif dev_id == self.self_device.device_id and pkt.is_command:
            h = self.servers[pkt.service_index]
            if h:
                # log(`handle pkt at ${h.name} cmd=${pkt.service_command}`)
                h.handle_packet_outer(pkt)
        else:
            if pkt.is_command:
                return  # it's a command, and it's not for us

            dev = None
            try:
                dev = next(d for d in self.devices if d.device_id == dev_id)
            except:
                pass

            if (pkt.service_index == JD_SERVICE_INDEX_CTRL):
                if (pkt.service_command == 0):
                    if (dev and dev.reset_count > (pkt.data[0] & 0xf)):
                        # if the reset counter went down, it means the device reseted;
                        # treat it as new device
                        log("device {} resetted", dev)
                        self.devices.remove(dev)
                        dev._destroy()
                        dev = None
                        self.emit(EV_RESTART)

                    matches = False
                    if not dev:
                        dev = Device(self, pkt.device_identifier, pkt.data)
                        # ask for uptime
                        # dev.send_ctrl_command(CMD_GET_REG | ControlReg.Uptime)
                        self.emit(EV_DEVICE_CONNECT, dev)
                    else:
                        matches = _service_matches(dev, pkt.data)
                        dev.services = pkt.data

                    if not matches:
                        self._reattach(dev)
                if dev:
                    dev.process_packet(pkt)
                return
            elif (pkt.service_index == JD_SERVICE_INDEX_CRC_ACK):
                # _got_ack(pkt)
                pass

            # we can't know the serviceClass,
            # no announcement seen yet for this device
            if not dev:
                return

            dev.process_packet(pkt)


class RawRegisterClient(EventEmitter):
    def __init__(self, client: 'Client', code: int) -> None:
        super().__init__(client.bus)
        self.code = code
        self._data: Optional[bytearray] = None
        self._refreshed_at = 0
        self.client = client

    def current(self, refresh_ms: int = 500):
        if self._refreshed_at + refresh_ms >= now():
            return self._data
        return None

    def _query(self):
        pkt = JDPacket(cmd=(CMD_GET_REG | self.code))
        self.client.send_cmd(pkt)

    def refresh(self):
        if self._refreshed_at < 0:
            return  # already in progress
        prev_data = self._data
        self._refreshed_at = -1

        def final_check():
            if prev_data is self._data:
                # if we still didn't get any data, emit "change" event, so that queries can time out
                self._data = None
                self._refreshed_at = 0
                self.emit(EV_CHANGE)

        def second_refresh():
            if prev_data is self._data:
                self._query()
                self.bus.taskq.delay(100, final_check)

        def first_refresh():
            if prev_data is self._data:
                self._query()
                self.bus.taskq.delay(50, second_refresh)

        self._query()
        self.bus.taskq.delay(20, first_refresh)

    async def query(self, refresh_ms: int = 500):
        curr = self.current(refresh_ms)
        if curr:
            return curr
        self.refresh()
        await self.event(EV_CHANGE)
        if self._data is None:
            raise RuntimeError(
                "Can't read reg #{} (from {})".format(self.code, self.client))
        return self._data

    def handle_packet(self, pkt: JDPacket):
        if pkt.is_reg_get and pkt.reg_code == self.code:
            self._data = pkt.data
            self._refreshed_at = now()
            self.emit(EV_CHANGE)


class Server(EventEmitter):
    def __init__(self, bus: Bus, service_class: int) -> None:
        super().__init__(bus)
        self.service_class = service_class
        self.instance_name: Optional[str] = None
        self.service_index = None
        self._status_code = 0  # u16, u16
        self.service_index = len(self.bus.servers)
        self.bus.servers.append(self)

    def status_code(self):
        return self._status_code

    def set_status_code(self, code: int, vendor_code: int):
        c = ((code & 0xffff) << 16) | (vendor_code & 0xffff)
        if c != self._status_code:
            self._status_code = c
            self.send_change_event()

    def handle_packet_outer(self, pkt: JDPacket):
        cmd = pkt.service_command
        if cmd == _JD_REG_STATUS_CODE | CMD_GET_REG:
            self.handle_status_code(pkt)
        elif cmd == _JD_REG_INSTANCE_NAME | CMD_GET_REG:
            self.handle_instance_name(pkt)
        else:
            # self.state_updated = False
            self.handle_packet(pkt)

    def handle_packet(self, pkt: JDPacket):
        pass

    def send_report(self, pkt: JDPacket):
        pkt.service_index = self.service_index
        pkt.device_identifier = self.bus.self_device.device_id
        self.bus._send_core(pkt)

    def send_event(self, event_code: int, data: bytes = None):
        pkt = JDPacket(cmd=self.bus.mk_event_cmd(event_code), data=data)
        def resend(): self.send_report(pkt)
        resend()
        self.bus.taskq.delay(20, resend)
        self.bus.taskq.delay(100, resend)

    def send_change_event(self):
        self.send_event(_JD_EV_CHANGE)
        self.emit(EV_CHANGE)

    def handle_status_code(self, pkt: JDPacket):
        self.handle_reg_u32(pkt, _JD_REG_STATUS_CODE, self._status_code)

    def handle_reg_u32(self, pkt: JDPacket, register: int, current: int):
        return self.handle_reg(pkt, register, "I", current)

    def handle_reg_i32(self, pkt: JDPacket, register: int, current: int):
        return self.handle_reg(pkt, register, "i", current)

    def handle_reg(self, pkt: JDPacket, register: int, fmt: str, current: RegType) -> RegType:
        getset = pkt.service_command >> 12
        if getset == 0 or getset > 2:
            return current
        reg = pkt.service_command & 0xfff
        if reg != register:
            return current
        if getset == 1:
            self.send_report(JDPacket.packed(
                pkt.service_command, fmt, current))
        else:
            if register >> 8 == 0x1:
                return current  # read-only
            v = pkt.unpack(fmt)
            if not isinstance(current, tuple):
                v = v[0]
            if v != current:
                self.state_updated = True
                current = cast(RegType, v)
        return current

    def handle_instance_name(self, pkt: JDPacket):
        self.send_report(JDPacket(cmd=pkt.service_command,
                         data=bytearray(self.instance_name or "", "utf-8")))

    def log(self, text: str, *args: object):
        prefix = "{}.{}>".format(self.bus.self_device,
                                 self.instance_name or self.service_index)
        log(prefix + text, *args)


class Client(EventEmitter):
    def __init__(self, bus: Bus, service_class: int, role: str) -> None:
        super().__init__(bus)
        self.broadcast = False
        self.service_class = service_class
        self.service_index = None
        self.device: Optional['Device'] = None
        self.current_device:  Optional['Device'] = None
        self.role = role
        self._registers: list[RawRegisterClient] = []
        bus.unattached_clients.append(self)
        bus.all_clients.append(self)

    def __str__(self) -> str:
        return "<Client '{}' srv:{} bnd:{}/{}>".format(
            self.role, util.hex_num(self.service_class),
            self.device and self.device.short_id, self.service_index)

    def _lookup_register(self, code: int):
        for reg in self._registers:
            if reg.code == code:
                return reg
        return None

    def register(self, code: int):
        r = self._lookup_register(code)
        if r is None:
            r = RawRegisterClient(self, code)
            self._registers.append(r)
        return r

    def handle_packet(self, pkt: JDPacket):
        pass

    def handle_packet_outer(self, pkt: JDPacket):
        if pkt.is_reg_get:
            r = self._lookup_register(pkt.reg_code)
            if r is not None:
                r.handle_packet(pkt)
        if pkt.is_event:
            self.emit(EV_EVENT, pkt)
        self.handle_packet(pkt)

    def send_cmd(self, pkt: JDPacket):
        if self.current_device is None:
            return
        pkt.service_index = self.service_index
        pkt.device_identifier = self.current_device.device_id
        pkt._header[3] |= JD_FRAME_FLAG_COMMAND
        self.bus._send_core(pkt)

    def on_attach(self):
        pass

    def _attach(self, dev: 'Device', service_idx: int):
        assert self.device is None
        if not self.broadcast:
            if not dev.matches_role_at(self.role, service_idx):
                return False
            self.device = dev
            self.service_index = service_idx
            self.bus.unattached_clients.remove(self)
        log("attached {}/{} to client {}", dev, service_idx, self.role)
        dev.clients.append(self)
        self.emit(EV_CONNECTED)
        return True

    def _detach(self):
        log("detached {}", self.role)
        self.service_index = None
        if not self.broadcast:
            assert self.device
            self.device = None
            self.bus.unattached_clients.append(self)
            self.bus.clear_attach_cache()
        self.emit(EV_DISCONNECTED)


_JD_CONTROL_ANNOUNCE_FLAGS_RESTART_COUNTER_STEADY = const(0xf)


class Device(EventEmitter):
    def __init__(self, bus: Bus, device_id: str, services: bytearray) -> None:
        super().__init__(bus)
        self.device_id = device_id
        self.services = services
        self.clients: list[Client] = []
        self.last_seen = now()
        self._event_counter: Optional[int] = None
        self._ctrl_client: Optional[Client] = None
        bus.devices.append(self)

    @property
    def ctrl_client(self):
        if self._ctrl_client is None:
            self._ctrl_client = Client(self.bus, 0, "")
            self._ctrl_client._attach(self, 0)
        return self._ctrl_client

    @property
    def announce_flags(self):
        return util.u16(self.services, 0)

    @property
    def reset_count(self):
        return self.announce_flags & _JD_CONTROL_ANNOUNCE_FLAGS_RESTART_COUNTER_STEADY

    @property
    def packet_count(self):
        return self.services[2]

    @property
    def is_connected(self):
        return self.clients != None

    @property
    def short_id(self):
        return util.short_id(self.device_id)

    def __str__(self) -> str:
        return "<JDDevice {}>".format(self.short_id)

    def debug_info(self):
        r = "Device: " + self.short_id + "; "
        for i in range(self.num_service_classes):
            s = self.service_class_at(i)
            assert s is not None
            r += util.hex_num(s) + ", "
        return r

    def service_class_at(self, idx: int):
        if idx == 0:
            return 0
        if idx < 0 or idx >= self.num_service_classes:
            return None
        return util.u32(self.services, idx << 2)

    def matches_role_at(self, role: str, service_idx: int):
        if not role or role == self.device_id or role == "{}:{}".format(self.device_id, service_idx):
            return True
        return True
        # return jacdac._rolemgr.getRole(self.deviceId, serviceIdx) == role

    @property
    def num_service_classes(self):
        return len(self.services) >> 2

    def _destroy(self):
        log("destroy " + self.short_id)
        for c in self.clients:
            c._detach()
        self.clients = None  # type: ignore

    def process_packet(self, pkt: JDPacket):
        self.last_seen = now()
        self.emit(EV_PACKET_RECEIVE, pkt)

        service_class = self.service_class_at(pkt.service_index)
        if not service_class or service_class == 0xffffffff:
            return

        if pkt.is_event:
            ec = self._event_counter
            if ec is None:
                ec = pkt.event_counter - 1
            ec += 1
            # how many packets ahead and behind current are we?
            ahead = (pkt.event_counter - ec) & CMD_EVENT_COUNTER_MASK
            behind = (ec - pkt.event_counter) & CMD_EVENT_COUNTER_MASK
            # ahead == behind == 0 is the usual case, otherwise
            # behind < 60 means self is an old event (or retransmission of something we already processed)
            # ahead < 5 means we missed at most 5 events, so we ignore self one and rely on retransmission
            # of the missed events, and then eventually the current event
            if ahead > 0 and (behind < 60 or ahead < 5):
                return
            # we got our event
            self.emit(EV_EVENT, pkt)
            self.bus.emit(EV_EVENT, pkt)
            self._event_counter = pkt.event_counter

        for c in self.clients:
            if (c.broadcast and c.service_class == service_class) or \
               (not c.broadcast and c.service_index == pkt.service_index):
                # log(`handle pkt at ${client.role} rep=${pkt.serviceCommand}`)
                c.current_device = self
                c.handle_packet_outer(pkt)
