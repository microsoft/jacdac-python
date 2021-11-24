from abc import abstractmethod
from asyncio.tasks import Task
import threading
import asyncio
import queue
import os
import time

from functools import reduce
from random import getrandbits, randrange
from typing import Any, Callable, Coroutine, Optional, Tuple, TypeVar, Union, cast, List, Dict
from textwrap import wrap

from .constants import *
from .logger.constants import *
from .control.constants import *
from .system.constants import *
from .role_manager.constants import *
from .unique_brain.constants import *
from .packet import *

from .util import now, log, logv
from .pack import PackTuple, PackType, jdpack, jdunpack

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

# _ACK_RETRIES = const(4)
# _ACK_DELAY = const(40)

RegType = TypeVar('RegType', bound=Union[PackType, PackTuple])
HandlerFn = Callable[..., Union[None, Coroutine[Any, Any, None]]]
EventHandlerFn = Callable[..., None]
UnsubscribeFn = Callable[..., None]


class EventEmitter:
    def __init__(self, bus: 'Bus') -> None:
        self.bus = bus

    def emit(self, id: str, *args: object):
        def add_cb(fn: HandlerFn):
            def cb():
                r = fn(*args)
                if r is None:
                    return
                # print(r)
                t = self.bus.loop.create_task(r)
                self.bus.pending_tasks.append(t)
                # print(t)
            self.bus.loop.call_soon(cb)

        self.bus.force_jd_thread()
        if not hasattr(self, "_listeners"):
            return
        idx = 0
        while idx < len(self._listeners):
            lid, fn, once = self._listeners[idx]
            if lid == id:
                # note that add_cb() can't be inlined here due to lack of block scope in Python
                add_cb(fn)
                if once:
                    del self._listeners[idx]
                    idx -= 1
            idx += 1

    def _init_emitter(self):
        if not hasattr(self, "_listeners"):
            self._listeners: List[Tuple[str, HandlerFn, bool]] = []

    def on(self, id: str, fn: HandlerFn) -> UnsubscribeFn:
        """Subscribes an event to a handler. Returns a callback to unsubscribe.

        Args:
            id (str): event identifier
            fn (HandlerFn): event callback
        Returns: callback to unsubscribe
        """
        self._init_emitter()
        self._listeners.append((id, fn, False))

        def unsubscribe():
            return self.off(id, fn)
        return unsubscribe

    def once(self, id: str, fn: HandlerFn):
        """Subscribes an event to run once; then get unsubscribed

        Args:
            id (str): event identifier
            fn (HandlerFn): event callback
        """
        self._init_emitter()
        self._listeners.append((id, fn, True))

    def off(self, id: str, fn: HandlerFn):
        """Unsubscribes a handler from an event

        Args:
            id (str): event identifier
            fn (HandlerFn): event callback
        """
        self._init_emitter()
        for i in range(len(self._listeners)):
            id2, fn2, _ign = self._listeners[i]
            if id == id2 and fn is fn2:
                del self._listeners[i]
                return
        raise ValueError("no matching on() for off()")

    # usage: await x.event("...")
    async def event(self, id: str):
        f = self.bus.loop.create_future()
        self.once(id, lambda: f.set_result(None))
        await f

    def wait_for(self, id: str):
        self.bus.force_non_jd_thread()
        cv = threading.Condition()
        happened = False

        def poke(*args: object):
            nonlocal happened
            with cv:
                happened = True
                cv.notify()

        self.once(id, poke)
        with cv:
            while not happened:
                cv.wait()

    def _log_report_prefix(self) -> str:
        return ""

    def _add_log_report(self, priority: int, text: str, *args: object):
        prefix = self._log_report_prefix()
        msg = prefix + text
        logger = self.bus.logger
        if logger:
            logger.report(priority, msg, *args)

    def log(self, text: str, *args: object):
        self._add_log_report(JD_LOGGER_PRIORITY_LOG, text, *args)

    def warn(self, text: str, *args: object):
        self._add_log_report(JD_LOGGER_PRIORITY_WARNING, text, *args)

    def debug(self, text: str, *args: object):
        self._add_log_report(JD_LOGGER_PRIORITY_DEBUG, text, *args)

    def error(self, text: str, *args: object):
        self._add_log_report(JD_LOGGER_PRIORITY_ERROR, text, *args)


def _service_matches(dev: 'Device', serv: bytearray):
    ds = dev.services
    if not ds or len(ds) != len(serv):
        return False
    for i in range(4, len(serv)):
        if ds[i] != serv[i]:
            return False
    return True


class Transport:
    """A base class for packet transports"""

    on_receive: Optional[Callable[[bytes], None]] = None
    # Callback to report a received packet to the bus

    def send(self, pkt: bytes) -> None:
        # send a packet payload over the transport layer
        pass

# TODO: replace randbytes


def rand_u64():
    return bytearray([getrandbits(8) for _ in range(8)])


class Bus(EventEmitter):
    """A Jacdac bus that managed devices, service client, registers."""

    def __init__(self, transport: Transport, *,
                 device_id: str = None,
                 product_identifier: int = None,
                 firmware_version: str = None,
                 device_description: str = None,
                 disable_logger: bool = False,
                 disable_role_manager: bool = False,
                 disable_brain: bool = False,
                 default_logger_min_priority: int = JD_LOGGER_PRIORITY_SILENT,
                 role_manager_file_name: str = "./.jacdac/roles.json",
                 settings_file_name: str = "./.jacdac/settings.json") -> None:
        """Instantiates a new Jacdac bus

        Args:
            transport (Transport): packet transport
            settings_file_name (str): Optional settings file location. Enables settings service.
            device_id (str, optional): Optional device identifier. Auto-generated if not specified.
            product_identifier (int, optional): Optional product identifier.
            device_description (str, optional): Optional device description.
            disable_logger (bool, optional): Disable the logger service. Defaults to False.
            disable_role_manager (bool, optional): Disable the role manager service. Defaults to False.
            disable_brain (bool, optional): Disable unique brain service. Defaults to False.
            default_logger_min_priority (int, optional): Optional mininimum logger priority. Defaults to JD_LOGGER_PRIORITY_SILENT.
        """
        super().__init__(self)
        self.devices: List['Device'] = []
        self.unattached_clients: List['Client'] = []
        self.all_clients: List['Client'] = []
        self.servers: List['Server'] = []
        self.logger: Optional[LoggerServer] = None
        self.role_manager: Optional[RoleManagerServer] = None
        self.pipes: List['InPipe'] = []

        self.product_identifier = product_identifier
        self.firmware_version = firmware_version
        self.device_description = device_description
        self.disable_brain = disable_brain
        self.disable_logger = disable_logger
        self.disable_role_manager = disable_role_manager
        self.default_logger_min_priority = default_logger_min_priority
        self.settings_file_name = settings_file_name
        self.role_manager_file_name = role_manager_file_name
        self._event_counter = 0

        if device_id is None:
            device_id = rand_u64().hex()
        self.self_device = Device(self, device_id, bytearray(4))
        self.process_thread = threading.Thread(target=self._process_task)
        self.transport = transport
        self._sendq: queue.Queue[bytes] = queue.Queue()
        self.pending_tasks: List[asyncio.Task[None]] = []

        self.loop = asyncio.new_event_loop()

        def handler(loop, context):  # type: ignore
            self.loop.default_exception_handler(context)  # type: ignore
            os._exit(10)
        self.loop.set_exception_handler(handler)  # type: ignore

        self.sender_thread = threading.Thread(target=self._sender)
        self.sender_thread.start()

        # self.taskq.recurring(2000, self.debug_dump)

        self.process_thread.start()

        self.log("starting bus, self={}", self.self_device)

    def run(self, cb: Callable[..., None], *args: Any):
        if self.process_thread is threading.current_thread():
            cb(*args)
        else:
            self.loop.call_soon(cb, *args)

    def _sender(self):
        while True:
            pkt = self._sendq.get()
            self.transport.send(pkt)

    def _process_task(self):
        loop = self.loop
        asyncio.set_event_loop(loop)

        # TODO: what's the best way to import these things
        ctrls = ControlServer(self)  # attach control server

        if not self.disable_logger:
            self.logger = LoggerServer(self)

        if not self.disable_role_manager:
            self.role_manager = RoleManagerServer(
                self, self.role_manager_file_name)

        if self.settings_file_name:
            from .settings.server import SettingsServer
            self.settings = SettingsServer(self)

        if not self.disable_brain:
            UniqueBrainServer(self)

        def keep_task(t: 'asyncio.Task[None]'):
            if t.done():
                t.result()  # throw exception if needed
                return False
            return True

        def announce():
            self.emit(EV_SELF_ANNOUNCE)
            self._gc_devices()
            ctrls.queue_announce()
            self.pending_tasks = [
                x for x in self.pending_tasks if keep_task(x)]
            loop.call_later(0.500, announce)
        loop.call_later(0.500, announce)

        def process_later(pkt: bytes):
            loop.call_soon_threadsafe(self.process_frame, pkt)
        self.transport.on_receive = process_later

        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    def process_frame(self, frame: bytes):
        if frame[2] - frame[12] < 4:
            # single packet in frame
            self.process_packet(JDPacket(frombytes=frame))
        else:
            # split into frames
            ptr = 12
            while ptr < 12 + frame[2]:
                sz = frame[ptr] + 4
                pktbytes = frame[0:12] + frame[ptr:ptr+sz]
                # log("PKT: {}-{} / {}", ptr, len(frame), pktbytes.hex())
                pkt = JDPacket(frombytes=pktbytes)
                if ptr > 12:
                    pkt.requires_ack = False
                self.process_packet(pkt)
                ptr += (sz + 3) & ~3

    def force_jd_thread(self):
        assert threading.current_thread() is self.process_thread

    def force_non_jd_thread(self):
        assert threading.current_thread() is not self.process_thread

    def debug_dump(self):
        print("Devices:")
        for dev in self.devices:
            info = dev.debug_info()
            if dev is self.self_device:
                info = "SELF: " + info
            print(info)
        print("END")

    def lookup_server(self, service_class: int) -> Optional['Server']:
        for s in self.servers:
            if s.service_class == service_class:
                return s
        return None

    def _gc_devices(self):
        now_ = now()
        cutoff = now_ - 2000
        self.self_device.last_seen = now_  # make sure not to gc self

        newdevs: List['Device'] = []
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
        pkt._header[2] = len(pkt._data) + 4
        buf = pkt._header + pkt._data
        crc = util.crc16(buf, 2)
        util.set_u16(buf, 0, crc)
        util.set_u16(pkt._header, 0, crc)
        self._sendq.put(buf)
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
        self.debug("reattaching services to {}; {}/{} to attach", dev,
                   len(self.unattached_clients), len(self.all_clients))
        new_clients: List['Client'] = []
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
        logv("route: {}", pkt)
        dev_id = pkt.device_id
        multi_command_class = pkt.multicommand_class
        service_index = pkt.service_index

        # TODO implement send queue for packet compression

        if pkt.requires_ack and pkt.device_id == self.self_device.device_id:
            ack = JDPacket(cmd=pkt.crc)
            ack.service_index = JD_SERVICE_INDEX_CRC_ACK
            ack.device_id = self.self_device.device_id
            self._send_core(ack)

        self.emit(EV_PACKET_PROCESS, pkt)

        if service_index == JD_SERVICE_INDEX_PIPE and pkt.device_id == self.self_device.device_id:
            port = pkt.service_command >> PIPE_PORT_SHIFT
            pipe = next(filter(lambda p: p.port == port, self.pipes), None)
            if pipe:
                pipe.handle_packet(pkt)
            else:
                self.debug("unknown pipe port {}", port)
            return

        if multi_command_class != None:
            if not pkt.is_command:
                return  # only commands supported in multi-command
            for h in self.servers:
                if h.service_class == multi_command_class:
                    # pretend it's directly addressed to us
                    pkt.device_id = self.self_device.device_id
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
                        self.debug("device resetted")
                        self.devices.remove(dev)
                        dev._destroy()
                        dev = None
                        self.emit(EV_RESTART)

                    matches = False
                    if not dev:
                        dev = Device(self, pkt.device_id, pkt.data)
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

    def add_pipe(self, pipe: 'InPipe'):
        port = randrange(1, 511)
        while any(p.port == port for p in self.pipes):
            port = randrange(1, 511)
        pipe.port = port
        self.pipes.append(pipe)

    def remove_pipe(self, pipe: 'InPipe'):
        if pipe in self.pipes:
            self.pipes.remove(pipe)


class InPipe(EventEmitter):
    """Incoming pipe"""

    def __init__(self, bus: Bus):
        super().__init__(bus)
        self.bus = bus
        self.port = -1
        self.next_cnt = 0
        self.closed = False
        self.in_q: List[bytearray] = []
        self.port = -1
        self.bus.add_pipe(self)

    def open_command(self, cmd: int):
        return JDPacket.packed(cmd, "b[8] u16 u16", bytearray.fromhex(self.bus.self_device.device_id), self.port, 0)

    def bytes_available(self) -> int:
        return reduce(lambda x, y: x + len(y), self.in_q, 0)

    def read(self) -> Optional[bytearray]:
        while True:
            if len(self.in_q):
                return self.in_q.pop(0)
            if self.closed:
                return None
            self.wait_for(EV_REPORT_RECEIVE)

    def _close(self):
        self.closed = True
        self.bus.remove_pipe(self)

    def close(self):
        self._close()
        self.in_q = []

    def meta(self, pkt: JDPacket):
        pass

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command
        if (cmd & PIPE_COUNTER_MASK) != (self.next_cnt & PIPE_COUNTER_MASK):
            return
        self.next_cnt += 1
        if cmd & PIPE_CLOSE_MASK:
            self._close()
        if cmd & PIPE_METADATA_MASK:
            self.meta(pkt)
        else:
            self.in_q.append(pkt.data)
            self.emit(EV_REPORT_RECEIVE)

    def read_list(self) -> List[bytearray]:
        r: List[bytearray] = []
        while True:
            buf = self.read()
            if not buf:
                break
            if len(buf):
                r.append(buf)
        return r


class OutPipe(EventEmitter):
    """Out going packet pipe"""

    def __init__(self, bus: 'Bus', pkt: JDPacket) -> None:
        super().__init__(bus)
        [device_id_bytes, port] = pkt.unpack("b[8] u16")

        self.device_id = cast(bytearray, device_id_bytes).hex()
        self.port = cast(int, port)
        self.next_cnt = 0

    @property
    def open(self):
        return not not self.port

    def write_ex(self, buf: bytearray, flags: int):
        if not self.port:
            return
        pkt = JDPacket(
            cmd=(self.next_cnt & PIPE_COUNTER_MASK) |
            (self.port << PIPE_PORT_SHIFT) |
            flags,
            data=buf
        )
        self.next_cnt += 1
        if flags & PIPE_CLOSE_MASK:
            self.port = None
        pkt.service_index = JD_SERVICE_INDEX_PIPE
        pkt.requires_ack = True
        pkt.device_id = self.device_id
        self.bus._send_core(pkt)
        # TODO: check acks
        # if not pkt._send_with_ack(self.device_id):
        #    self.port = None
        #    throw "out pipe error: no ACK"

    def write(self, buf: bytearray):
        self.write_ex(buf, 0)

    def write_and_close(self, buf: bytearray):
        self.write_ex(buf, PIPE_CLOSE_MASK)

    def close(self):
        self.write_and_close(bytearray(0))

    def write_meta(self, buf: bytearray):
        self.write_ex(buf, PIPE_METADATA_MASK)


class RawRegisterClient(EventEmitter):
    """A Jacdac register client
    """

    def __init__(self, client: 'Client', code: int, pack_format: Optional[str]) -> None:
        super().__init__(client.bus)
        self.code = code
        self._data: Optional[bytearray] = None
        self._refreshed_at = 0
        self.client = client
        self.pack_format = pack_format
        self.not_implemented = False

    def clear(self):
        self._data = None
        self._refreshed_at = 0
        self.not_implemented = False

    def current(self, refresh_ms: int = -1):
        if refresh_ms < 0 or self._refreshed_at + refresh_ms >= now():
            return self._data
        return None

    def values(self) -> Optional[PackTuple]:
        data = self.query_no_wait()
        if data and self.pack_format:
            return jdunpack(data, self.pack_format)
        return None

    def set_values(self, *args: PackType):
        if self.pack_format is None:
            raise RuntimeError("set_value not supported")
        if not self.client.connected:
            return

        data = jdpack(self.pack_format, *args)

        def send():
            pkt = JDPacket(cmd=JD_SET(self.code), data=data)
            self.client.send_cmd(pkt)
            self.refresh()

        self.bus.run(send)

    def value(self, default_value: Any = None) -> Optional[Any]:
        """Extracts the value of the first field."""
        values = self.values()
        if values is None:
            return default_value
        else:
            return values[0]

    def bool_value(self, default_value: bool = None) -> Optional[bool]:
        """Extracts the value of the first field as a boolean."""
        value = self.value()
        return bool(value) if not value is None else default_value

    def float_value(self, default_value: float = None, scale: int = 1) -> Optional[float]:
        value = self.value()
        return float(value) * scale if not value is None else default_value

    def _query(self):
        if not self.client.connected:
            return
        pkt = JDPacket(cmd=JD_GET(self.code))
        self.client.send_cmd(pkt)

    def refresh(self):
        if not self.client.connected or self._refreshed_at < 0 or self.not_implemented:
            return  # already in progress

        def do_refresh():
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
                    self.bus.loop.call_later(0.100, final_check)

            def first_refresh():
                if prev_data is self._data:
                    self._query()
                    self.bus.loop.call_later(0.050, second_refresh)

            self._query()
            self.bus.loop.call_later(0.020, first_refresh)

        self.bus.run(do_refresh)

    # can't be called from event handlers!
    def query(self, refresh_ms: int = 500):
        if self.not_implemented:
            return None
        curr = self.current(refresh_ms)
        if curr:
            return curr
        self.refresh()
        self.wait_for(EV_CHANGE)
        if self._data is None:
            raise RuntimeError(
                "Can't read reg #{} (from {})".format(hex(self.code), self.client))
        return self._data

    async def query_async(self, refresh_ms: int = 500):
        if self.not_implemented:
            return None
        curr = self.current(refresh_ms)
        if curr:
            return curr
        self.refresh()
        # todo: test if changed
        await self.event(EV_CHANGE)
        if self._data is None:
            raise RuntimeError(
                "Can't read reg #{} (from {})".format(hex(self.code), self.client))
        return self._data

    def query_no_wait(self, refresh_ms: int = -1):
        if self.not_implemented:
            return None
        curr = self.current(refresh_ms)
        if curr:
            return curr
        self.refresh()
        return self._data

    def handle_packet(self, pkt: JDPacket):
        if self.not_implemented:
            return
        if pkt.is_reg_get and pkt.reg_code == self.code:
            self._data = pkt.data
            self._refreshed_at = now()
            self.emit(EV_CHANGE)


class Server(EventEmitter):
    def __init__(self, bus: Bus, service_class: int, *, instance_name: str = None) -> None:
        super().__init__(bus)
        self.service_class = service_class
        self.instance_name = instance_name
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
        if cmd == JD_GET(JD_REG_STATUS_CODE):
            self.handle_status_code(pkt)
        elif cmd == JD_GET(JD_REG_INSTANCE_NAME):
            self._handle_instance_name(pkt)
        else:
            # self.state_updated = False
            self.handle_packet(pkt)

    def handle_packet(self, pkt: JDPacket):
        pass

    def send_report(self, pkt: JDPacket):
        pkt.service_index = self.service_index
        pkt.device_id = self.bus.self_device.device_id
        self.bus._send_core(pkt)

    def send_event(self, event_code: int, data: bytes = None):
        pkt = JDPacket(cmd=self.bus.mk_event_cmd(event_code), data=data)
        def resend(): self.send_report(pkt)

        def trisend():
            resend()
            self.bus.loop.call_later(0.020, resend)
            self.bus.loop.call_later(0.100, resend)

        self.bus.run(trisend)

    def send_change_event(self):
        self.send_event(JD_EV_CHANGE)
        self.emit(EV_CHANGE)

    def handle_status_code(self, pkt: JDPacket):
        self.handle_reg_u32(pkt, JD_REG_STATUS_CODE, self._status_code)

    def handle_reg_u8(self, pkt: JDPacket, register: int, current: int):
        return self.handle_reg(pkt, register, "u8", current)

    def handle_reg_u32(self, pkt: JDPacket, register: int, current: int):
        return self.handle_reg(pkt, register, "u32", current)

    def handle_reg_i32(self, pkt: JDPacket, register: int, current: int):
        return self.handle_reg(pkt, register, "i32", current)

    def handle_reg(self, pkt: JDPacket, register: int, fmt: str, current: RegType) -> RegType:
        getset = pkt.service_command >> 12
        if getset == 0 or getset > 2:
            return current
        reg = pkt.service_command & 0xfff
        if reg != register:
            return current
        if getset == 1:
            if isinstance(current, tuple):
                self.send_report(JDPacket.packed(
                    pkt.service_command, fmt, *current))
            else:
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

    def _handle_instance_name(self, pkt: JDPacket):
        self.send_report(JDPacket(cmd=pkt.service_command,
                         data=bytearray(self.instance_name or "", "utf-8")))

    def _log_report_prefix(self) -> str:
        return "{}.{}>".format(self.bus.self_device,
                               self.instance_name or self.service_index)


class SensorServer(Server):
    def __init__(self, bus: Bus, service_class: int, streaming_interval: int, *, instance_name: str = None, streaming_preferred_interval: int = None) -> None:
        super().__init__(bus, service_class, instance_name=instance_name)
        self.streaming_samples: int = 0
        self.streaming_preferred_interval: Optional[int] = streaming_preferred_interval
        self.streaming_interval = streaming_interval
        self._stream_task: Optional[Task[None]] = None

    @abstractmethod
    def send_reading(self):
        pass

    def _start_streaming(self):
        if self.streaming_samples > 0 and not self._stream_task:
            self._stream_task = asyncio.ensure_future(self._stream())

    async def _stream(self):
        while(self.streaming_samples > 0):
            self.streaming_samples = self.streaming_samples - 1
            self.send_reading()
            interval = max(20, self.streaming_interval)
            await asyncio.sleep(interval / 1000)
        self._stream_task = None

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command
        if cmd == JD_GET(JD_REG_STREAMING_SAMPLES) or cmd == JD_SET(JD_REG_STREAMING_SAMPLES):
            self._handle_streaming_samples(pkt)
        elif cmd == JD_GET(JD_REG_STREAMING_INTERVAL) or cmd == JD_SET(JD_REG_STREAMING_SAMPLES):
            self._handle_streaming_interval(pkt)
        elif cmd == JD_GET(JD_REG_STREAMING_PREFERRED_INTERVAL):
            self._handle_streaming_preferred_interval(pkt)
        super().handle_packet(pkt)

    def _handle_streaming_samples(self, pkt: JDPacket):
        self.streaming_samples = self.handle_reg_u8(pkt, JD_REG_STREAMING_SAMPLES,
                                                    self.streaming_samples)
        self._start_streaming()

    def _handle_streaming_interval(self, pkt: JDPacket):
        self.streaming_interval = self.handle_reg_u32(
            pkt, JD_REG_STREAMING_INTERVAL, self.streaming_interval)

    def _handle_streaming_preferred_interval(self, pkt: JDPacket):
        if self.streaming_preferred_interval:
            self.handle_reg_u32(
                pkt, JD_REG_STREAMING_PREFERRED_INTERVAL, self.streaming_preferred_interval)
        else:
            self.send_report(pkt.not_implemented())


class ControlServer(Server):
    """A server for the control service, used internally by the bus."""

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
        buf = jdpack("u32[]", *ids)
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
            reg_code = pkt.reg_code
            if reg_code == JD_CONTROL_REG_UPTIME:
                self.send_report(JDPacket.packed(
                    JD_GET(JD_CONTROL_REG_UPTIME), "u64",  time.monotonic_ns() // 1000))
            elif self.bus.product_identifier and reg_code == JD_CONTROL_REG_PRODUCT_IDENTIFIER:
                self.send_report(JDPacket.packed(
                    JD_GET(JD_CONTROL_REG_PRODUCT_IDENTIFIER), "u32", self.bus.product_identifier))
            elif self.bus.firmware_version and reg_code == JD_CONTROL_REG_FIRMWARE_VERSION:
                self.send_report(JDPacket.packed(
                    JD_GET(JD_CONTROL_REG_PRODUCT_IDENTIFIER), "s", self.bus.firmware_version))
            elif reg_code == JD_CONTROL_REG_DEVICE_DESCRIPTION:
                uname = os.uname()
                descr = "{}, {}, {}, {}, jacdac {}".format(
                    self.bus.device_description or "",
                    uname.nodename, uname.sysname, uname.release, JD_VERSION)
                self.send_report(JDPacket.packed(
                    JD_GET(JD_CONTROL_REG_DEVICE_DESCRIPTION), "s", descr))
            else:
                self.send_report(pkt.not_implemented())
        else:
            cmd = pkt.service_command
            if cmd == JD_CONTROL_CMD_SERVICES:
                self.queue_announce()
            elif cmd == JD_CONTROL_CMD_IDENTIFY:
                self.bus.emit(EV_IDENTIFY)
            elif cmd == JD_CONTROL_CMD_RESET:
                # TODO: reset support
                raise RuntimeError("reset requested")
            else:
                self.send_report(pkt.not_implemented())


class LoggerServer(Server):

    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_LOGGER)
        self.min_priority = self.bus.default_logger_min_priority
        self._last_listener_time = 0

    def handle_packet(self, pkt: JDPacket):
        self.min_priority = self.handle_reg_u8(
            pkt, JD_LOGGER_REG_MIN_PRIORITY, self.min_priority)
        cmd = pkt.service_command
        if cmd == JD_SET(JD_LOGGER_REG_MIN_PRIORITY):
            d = cast(int, pkt.unpack("u8")[0])
            self._last_listener_time = now()
            if d < self.min_priority:
                self.min_priority = d
        return super().handle_packet(pkt)

    def report(self, priority: int, msg: str, *args: object):
        log(msg, *args)
        cmd: int = -1
        if priority == JD_LOGGER_PRIORITY_DEBUG:
            cmd = JD_LOGGER_CMD_DEBUG
        elif priority == JD_LOGGER_PRIORITY_LOG:
            cmd = JD_LOGGER_CMD_LOG
        elif priority == JD_LOGGER_PRIORITY_WARNING:
            cmd = JD_LOGGER_CMD_WARN
        elif priority == JD_LOGGER_CMD_ERROR:
            cmd = JD_LOGGER_CMD_ERROR
        else:
            return

        if now() - self._last_listener_time > JD_LOGGER_LISTENER_TIMEOUT:
            self._last_listener_time = 0
            self.min_priority = self.bus.default_logger_min_priority

        if not msg or not self._last_listener_time or priority < self.min_priority:
            return

        chunks = wrap(msg, JD_SERIAL_MAX_PAYLOAD_SIZE)

        def send_chunks():
            for chunk in chunks:
                self.send_report(JDPacket.packed(cmd, "s", chunk))

        self.bus.run(send_chunks)


class UniqueBrainServer(Server):
    """A server for the unique brain service, used internally by the bus"""

    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_UNIQUE_BRAIN)


class RoleManagerServer(Server):
    def __init__(self, bus: Bus, file_name: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_ROLE_MANAGER)

        from jacdac.settings_file import SettingsFile
        self.settings = SettingsFile(file_name)
        self.auto_bind = 1

    def handle_packet(self, pkt: JDPacket):
        self.auto_bind = self.handle_reg_u8(
            pkt, JD_ROLE_MANAGER_REG_AUTO_BIND, self.auto_bind)

        cmd = pkt.service_command

        if cmd == JD_ROLE_MANAGER_CMD_LIST_REQUIRED_ROLES:
            self.handle_list_required_roles(pkt)
        elif cmd == JD_ROLE_MANAGER_CMD_LIST_STORED_ROLES:
            self.handle_list_stored_roles(pkt)
        elif cmd == JD_ROLE_MANAGER_CMD_CLEAR_ALL_ROLES:
            self.handle_clear_all_roles(pkt)
        elif cmd == JD_ROLE_MANAGER_CMD_GET_ROLE:
            self.handle_get_role(pkt)
        elif cmd == JD_ROLE_MANAGER_CMD_SET_ROLE:
            self.handle_set_role(pkt)
        elif cmd == JD_GET(JD_ROLE_MANAGER_REG_ALL_ROLES_ALLOCATED):
            self.handle_all_roles_allocated(pkt)
        else:
            super().handle_packet(pkt)

    def handle_list_required_roles(self, pkt: JDPacket):
        pipe = OutPipe(self.bus, pkt)
        for client in self.bus.all_clients:
            device_id = bytearray(0)
            service_class = client.service_class
            service_index = client.service_index or 0
            role = client.role
            if client.device:
                device_id = bytearray.fromhex(client.device.device_id)
            payload = jdpack("b[8] u32 u8 s", device_id,
                             service_class, service_index, role)
            pipe.write(bytearray(payload))
        pipe.close()

    def handle_list_stored_roles(self, pkt: JDPacket):
        pipe = OutPipe(self.bus, pkt)
        for role in self.settings.list():
            payload = self.settings.read(role)
            pipe.write(payload)
        pipe.close()

    def handle_clear_all_roles(self, pkt: JDPacket):
        self.settings.clear()
        self.send_change_event()

    def handle_get_role(self, pkt: JDPacket):
        payload = pkt.unpack("b[8] u8")
        device_id_b = cast(bytearray, payload[0])
        device_id = device_id_b.hex()
        service_index = cast(int, payload[1])

        role = ""
        for client in self.bus.all_clients:
            if client.device and client.device.device_id == device_id and client.service_index == service_index:
                role = client.role
                break
        self.send_report(JDPacket.packed(
            JD_ROLE_MANAGER_CMD_GET_ROLE, "u[8] u8 s", device_id_b, service_index, role))

    def handle_set_role(self, pkt: JDPacket):
        payload = pkt.unpack("b[8] u8 s")
        device_id_b = cast(bytearray, payload[0])
        device_id = device_id_b.hex()
        service_index = cast(int, payload[1])
        role = cast(str, payload[2])
        self.send_change_event()
        # TODO

    def handle_all_roles_allocated(self, pkt: JDPacket):
        res = 0 if len(self.bus.unattached_clients) > 0 else 1
        self.send_report(JDPacket.packed(pkt.service_command, "u8", res))


class Client(EventEmitter):
    """Base class to define service clients."""

    def __init__(self, bus: Bus, service_class: int, pack_formats: Dict[int, str], role: str) -> None:
        super().__init__(bus)
        self.broadcast = False
        self.service_class = service_class
        self.pack_formats = pack_formats
        self.service_index = None
        self.device: Optional['Device'] = None
        self.role = role
        self._registers: List[RawRegisterClient] = []
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

    @property
    def connected(self) -> bool:
        """Indicates if the client is a connected to a server"""
        return True if self.device else False

    def register(self, code: int):
        """Retreives the register by code"""
        r = self._lookup_register(code)
        if r is None:
            pack_format = self._lookup_packformat(code)
            r = RawRegisterClient(self, code, pack_format)
            self._registers.append(r)
        return r

    def _lookup_packformat(self, code: int) -> Optional[str]:
        if code in self.pack_formats:
            return self.pack_formats[code]
        return None

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
        """Sends a command packet to the server"""
        if self.device is None:
            return
        pkt.service_index = self.service_index
        pkt.device_id = self.device.device_id
        pkt._header[3] |= JD_FRAME_FLAG_COMMAND

        self.bus.run(self.bus._send_core, pkt)

    def send_cmd_packed(self, cmd: int, *args: PackType):
        if args is None:
            pkt = JDPacket(cmd=cmd)
        else:
            if not cmd in self.pack_formats:
                raise RuntimeError("unknown data format")
            fmt = self.pack_formats[cmd]
            data = jdpack(fmt, *args)
            pkt = JDPacket(cmd=cmd, data=data)
        self.send_cmd(pkt)

    def _attach(self, dev: 'Device', service_idx: int):
        assert self.device is None
        if not self.broadcast:
            if not dev.matches_role_at(self.role, service_idx):
                return False
            self.device = dev
            self.service_index = service_idx
            self.bus.unattached_clients.remove(self)
        self.debug("attached {}/{} to client {}", dev, service_idx, self.role)
        dev.clients.append(self)
        self.emit(EV_CONNECTED)
        if self.bus.role_manager:
            self.bus.role_manager.send_change_event()

        return True

    def _detach(self):
        self.debug("detached")
        self.service_index = None
        if not self.broadcast:
            assert self.device
            self.device = None
            for reg in self._registers:
                reg.clear()
            self.bus.unattached_clients.append(self)
            self.bus.clear_attach_cache()
        self.emit(EV_DISCONNECTED)
        if self.bus.role_manager:
            self.bus.role_manager.send_change_event()

    def on_connect(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """Registers an event handler when the client connects to a server

        Args:
            handler (EventHandlerFn): function to run with client connects

        Returns:
            UnsubscribeFn: function to call to unregister handler
        """
        return self.on(EV_CONNECTED, handler)

    def on_disconnect(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """Registers an event handler when the client disconnects from a server

        Args:
            handler (EventHandlerFn): function to run with client connects

        Returns:
            UnsubscribeFn: function to call to unregister handler
        """
        return self.on(EV_DISCONNECTED, handler)

    def on_event(self, code: int, handler: EventHandlerFn) -> UnsubscribeFn:
        """Registers an event handler for the given event code

        Args:
            code (int): event identifier code
            handler (EventHandlerFn): function to run with decoded event data and packet

        Returns:
            UnsubscribeFn: function to call to unregister handler
        """
        if code in self.pack_formats:
            fmt = self.pack_formats[code]
        else:
            fmt = None

        def cb(pkt: JDPacket) -> None:
            if pkt.event_code == code:
                if fmt is None:
                    data = []
                else:
                    data = jdunpack(pkt.data, fmt)
                handler(data)
        return self.on(EV_EVENT, cb)

    def _log_report_prefix(self) -> str:
        return "{}:{}>".format(self.bus.self_device, self.role)


class SensorClient(Client):
    """A client for a sensor service"""

    def __init__(self, bus: Bus, service_class: int, pack_formats: Dict[int, str], role: str, *, preferred_interval: int = None) -> None:
        super().__init__(bus, service_class, pack_formats, role)
        self.preferred_interval = preferred_interval

    @property
    def streaming_samples(self) -> Optional[int]:
        """Queries the current estimated streaming samples value"""
        return self.register(JD_REG_STREAMING_SAMPLES).value()

    @property
    def streaming_interval(self) -> Optional[int]:
        return self.register(JD_REG_STREAMING_INTERVAL).value()

    @property
    def streaming_preferred_interval(self) -> Optional[int]:
        return self.register(JD_REG_STREAMING_PREFERRED_INTERVAL).value()

    def refresh_reading(self) -> None:
        if self._should_refresh_streaming_samples():
            self.register(JD_REG_STREAMING_SAMPLES).set_values(0xff)

    def _lookup_packformat(self, code: int) -> Optional[str]:
        if code == JD_REG_STREAMING_SAMPLES:
            return "u8"
        elif code == JD_REG_STREAMING_INTERVAL:
            return "u32"
        elif code == JD_REG_STREAMING_PREFERRED_INTERVAL:
            return "u32"
        return Client._lookup_packformat(self, code)

    def _should_refresh_streaming_samples(self) -> bool:
        readingReg = self.register(JD_REG_READING)
        if readingReg._refreshed_at < 0:
            # refresh in progress
            return False

        samplesReg = self.register(JD_REG_STREAMING_SAMPLES)
        if samplesReg._refreshed_at < 0:
            # refresh in progress
            return False

        samples = samplesReg.value()
        # check if we have some value
        MIN_SAMPLES = 16
        if samples is None or samples < MIN_SAMPLES:
            return True

        interval = self._reading_interval()

        # haven't seen samples in a while
        if now() > readingReg._refreshed_at + 3 * interval:
            return True

        # check if the streaming is consumed
        if now() > samplesReg._refreshed_at + max(0, samples - MIN_SAMPLES) * interval:
            return True
        return False

    def _reading_interval(self) -> int:
        """Resolves the best refresh interval for streaming"""
        interval = self.streaming_interval
        if interval:
            return interval
        interval = self.streaming_preferred_interval
        if interval:
            return interval
        if self.preferred_interval:
            return self.preferred_interval
        return JD_STREAMING_DEFAULT_INTERVAL


class Device(EventEmitter):
    """A device on the bus"""

    def __init__(self, bus: Bus, device_id: str, services: bytearray) -> None:
        super().__init__(bus)
        self.device_id = device_id
        self.services = services
        self.clients: List[Client] = []
        self.last_seen = now()
        self._event_counter: Optional[int] = None
        self._ctrl_client: Optional[Client] = None
        bus.devices.append(self)

    @property
    def ctrl_client(self):
        if self._ctrl_client is None:
            self._ctrl_client = Client(
                self.bus, JD_SERVICE_CLASS_CONTROL, JD_CONTROL_PACK_FORMATS, "")
            self._ctrl_client._attach(self, 0)
        return self._ctrl_client

    @property
    def announce_flags(self):
        return util.u16(self.services, 0)

    @property
    def reset_count(self):
        return self.announce_flags & JD_CONTROL_ANNOUNCE_FLAGS_RESTART_COUNTER_STEADY

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
        # TODO: return jacdac._rolemgr.getRole(self.deviceId, serviceIdx) == role

    @property
    def num_service_classes(self):
        return len(self.services) >> 2

    def _destroy(self):
        self.debug("destroy")
        for c in self.clients:
            c._detach()
        self.clients = None  # type: ignore

    def _log_report_prefix(self) -> str:
        return "{}>".format(self.short_id)

    def process_packet(self, pkt: JDPacket):
        self.last_seen = now()
        self.emit(EV_PACKET_RECEIVE, pkt)

        if pkt.service_command == JD_CMD_COMMAND_NOT_IMPLEMENTED:
            cmd = util.u16(pkt.data, 0)
            if cmd >> 12 == CMD_GET_REG >> 12:
                reg_code = cmd & CMD_REG_MASK
                srv_index = pkt.service_index
                for c in self.clients:
                    if c.service_index == srv_index:
                        c.register(reg_code).not_implemented = True
                        break
            return

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
                c.device = self
                c.handle_packet_outer(pkt)
