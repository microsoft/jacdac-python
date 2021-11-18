# Autogenerated constants for TCP service
from enum import IntEnum
from jacdac.constants import *
JD_SERVICE_CLASS_TCP = const(0x1b43b70b)


class TcpTcpError(IntEnum):
    INVALID_COMMAND = const(0x1)
    INVALID_COMMAND_PAYLOAD = const(0x2)


JD_TCP_CMD_OPEN = const(0x80)
JD_TCP_PIPE_OPEN_SSL = const(0x1)
JD_TCP_PIPE_ERROR = const(0x0)
JD_TCP_PACK_FORMATS = {
    JD_TCP_CMD_OPEN: "b[12]",
    JD_TCP_PIPE_OPEN_SSL: "u16 s",
    JD_TCP_PIPE_ERROR: "i32"
}
