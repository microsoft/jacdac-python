def const(v: int): return v
# A shim for the micropython const keyword

JD_VERSION = "0.1.1"

JD_SERIAL_HEADER_SIZE = const(16)
JD_SERIAL_MAX_PAYLOAD_SIZE = const(236)
JD_SERVICE_INDEX_MASK = const(0x3f)
JD_SERVICE_INDEX_INV_MASK = const(0xc0)
JD_SERVICE_INDEX_CRC_ACK = const(0x3f)
JD_SERVICE_INDEX_PIPE = const(0x3e)
JD_SERVICE_INDEX_CTRL = const(0x00)

JD_FRAME_FLAG_COMMAND = const(0x01)
JD_FRAME_FLAG_ACK_REQUESTED = const(0x02)
JD_FRAME_FLAG_IDENTIFIER_IS_SERVICE_CLASS = const(0x04)

JD_REGISTER_POLL_STREAMING_INTERVAL = 5000
JD_REGISTER_POLL_FIRST_REPORT_INTERVAL = 400
JD_REGISTER_POLL_REPORT_INTERVAL = 5001
JD_REGISTER_POLL_REPORT_MAX_INTERVAL = 60000
JD_REGISTER_POLL_REPORT_VOLATILE_INTERVAL = 1000
JD_REGISTER_POLL_REPORT_VOLATILE_MAX_INTERVAL = 5000
JD_REGISTER_OPTIONAL_POLL_COUNT = 3
JD_STREAMING_DEFAULT_INTERVAL = 50

JD_LOGGER_LISTENER_TIMEOUT = 3000

# Registers 0x001-0x07f - r/w common to all services
# Registers 0x080-0x0ff - r/w defined per-service
# Registers 0x100-0x17f - r/o common to all services
# Registers 0x180-0x1ff - r/o defined per-service
# Registers 0x200-0xeff - custom, defined per-service
# Registers 0xf00-0xfff - reserved for implementation, should not be on the wire

CMD_GET_REG = const(0x1000)
CMD_SET_REG = const(0x2000)
CMD_TYPE_MASK = const(0xf000)
CMD_REG_MASK = const(0x0fff)
CMD_EVENT_MASK = const(0x8000)
CMD_EVENT_CODE_MASK = const(0xff)
CMD_EVENT_COUNTER_MASK = const(0x7f)
CMD_EVENT_COUNTER_POS = const(8)

PIPE_PORT_SHIFT = const(7)
PIPE_COUNTER_MASK = const(0x001f)
PIPE_CLOSE_MASK = const(0x0020)
PIPE_METADATA_MASK = (0x0040)

DEVTOOLS_URL = "http://localhost:8081"
DEVTOOLS_SOCKET_URL = "ws://localhost:8081"

def JD_GET(code: int):
    assert 0 <= code and code <= 0xfff
    return CMD_GET_REG | code


def JD_SET(code: int):
    assert 0 <= code and code <= 0xfff
    return CMD_SET_REG | code
