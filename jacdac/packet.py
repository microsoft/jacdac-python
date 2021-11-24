from typing import Any, Optional

from .pack import PackType, jdpack, jdunpack
from .constants import *
from .system.constants import JD_CMD_COMMAND_NOT_IMPLEMENTED
import jacdac.util as util


class JDPacket:
    """A Jacdac packet
    """

    def __init__(self, *, cmd: int = None, size: int = 0, frombytes: bytes = None, data: bytes = None, sender: Any = None) -> None:
        self.timestamp = util.now()
        if frombytes is None:
            self._header = bytearray(JD_SERIAL_HEADER_SIZE)
            self.data = bytearray(data or size)
        else:
            self._header = bytearray(frombytes[0:JD_SERIAL_HEADER_SIZE])
            self.data = bytearray(frombytes[JD_SERIAL_HEADER_SIZE:])
        if cmd is not None:
            self.service_command = cmd
        self.sender = sender

    @staticmethod
    def packed(cmd: int, fmt: str, *args: PackType):
        return JDPacket(cmd=cmd, data=jdpack(fmt, *args))

    def unpack(self, fmt: str):
        return jdunpack(self.data, fmt)

    @property
    def service_command(self):
        return util.u16(self._header, 14)

    @service_command.setter
    def service_command(self, cmd: int):
        util.set_u16(self._header, 14, cmd)

    @property
    def device_id(self) -> str:
        return util.buf2hex(self._header[4:12])

    @device_id.setter
    def device_id(self, id_str: str):
        id = util.hex2buf(id_str)
        if len(id) != 8:
            raise ValueError()
        self._header[4:12] = id

    @property
    def packet_flags(self):
        return self._header[3]

    @property
    def multicommand_class(self):
        if self.packet_flags & JD_FRAME_FLAG_IDENTIFIER_IS_SERVICE_CLASS:
            return util.u32(self._header, 4)
        else:
            return None

    @property
    def size(self):
        return self._header[12]

    @property
    def requires_ack(self):
        return (self.packet_flags & JD_FRAME_FLAG_ACK_REQUESTED) != 0

    @requires_ack.setter
    def requires_ack(self, val: bool):
        if val != self.requires_ack:
            self._header[3] ^= JD_FRAME_FLAG_ACK_REQUESTED

    @property
    def service_index(self):
        return self._header[13] & JD_SERVICE_INDEX_MASK

    @property
    def is_regular_service(self):
        return self.service_index <= 58

    @service_index.setter
    def service_index(self, val:  Optional[int]):
        if val is None:
            raise ValueError("service_index not set")
        self._header[13] = (self._header[13] & JD_SERVICE_INDEX_INV_MASK) | val

    @property
    def crc(self):
        return util.u16(self._header, 0)

    @property
    def is_event(self):
        return self.is_report and self.is_regular_service and (self.service_command & CMD_EVENT_MASK) != 0

    @property
    def event_code(self):
        assert self.is_event
        return self.service_command & CMD_EVENT_CODE_MASK

    @property
    def event_counter(self):
        assert self.is_event
        return (self.service_command >> CMD_EVENT_COUNTER_POS) & CMD_EVENT_COUNTER_MASK

    @property
    def is_reg_set(self):
        return self.is_regular_service and self.service_command >> 12 == CMD_SET_REG >> 12

    @property
    def is_reg_get(self):
        return self.is_regular_service and self.service_command >> 12 == CMD_GET_REG >> 12

    @property
    def reg_code(self):
        return self.service_command & CMD_REG_MASK

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, buf: bytearray):
        if len(buf) > JD_SERIAL_MAX_PAYLOAD_SIZE:
            raise ValueError("Too big")
        self._header[12] = len(buf)
        self._data = buf

    @property
    def is_command(self):
        return (self.packet_flags & JD_FRAME_FLAG_COMMAND) != 0

    @property
    def is_report(self):
        return (self.packet_flags & JD_FRAME_FLAG_COMMAND) == 0

    def to_string(self):
        msg = "{}/{}[{}]: {} sz={}".format(
            util.short_id(self._header[4:12]),
            self.service_index,
            self.packet_flags,
            util.hex_num(self.service_command, 4),
            self.size)
        if self.size < 20:
            msg += ": " + util.buf2hex(self.data)
        else:
            msg += ": " + util.buf2hex(self.data[0:20]) + "..."
        return msg

    def __str__(self):
        return "<JDPacket {}>".format(self.to_string())

    def not_implemented(self):
        return JDPacket.packed(JD_CMD_COMMAND_NOT_IMPLEMENTED, "u16 u16", self.service_command, self.crc)
