def const(v: int): return v
    # A shim for the micropython const keyword

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

# Registers 0x001-0x07f - r/w common to all services
# Registers 0x080-0x0ff - r/w defined per-service
# Registers 0x100-0x17f - r/o common to all services
# Registers 0x180-0x1ff - r/o defined per-service
# Registers 0x200-0xeff - custom, defined per-service
# Registers 0xf00-0xfff - reserved for implementation, should not be on the wire

JD_READING_THRESHOLD_NEUTRAL = const(0x1)
JD_READING_THRESHOLD_INACTIVE = const(0x2)
JD_READING_THRESHOLD_ACTIVE = const(0x3)
JD_STATUS_CODES_READY = const(0x0)
JD_STATUS_CODES_INITIALIZING = const(0x1)
JD_STATUS_CODES_CALIBRATING = const(0x2)
JD_STATUS_CODES_SLEEPING = const(0x3)
JD_STATUS_CODES_WAITING_FOR_INPUT = const(0x4)
JD_STATUS_CODES_CALIBRATION_NEEDED = const(0x64)
JD_CMD_ANNOUNCE = const(0x0)
JD_CMD_EVENT = const(0x1)
JD_CMD_CALIBRATE = const(0x2)
JD_REG_INTENSITY = const(0x1)
JD_REG_VALUE = const(0x2)
JD_REG_MIN_VALUE = const(0x110)
JD_REG_MAX_VALUE = const(0x111)
JD_REG_MAX_POWER = const(0x7)
JD_REG_STREAMING_SAMPLES = const(0x3)
JD_REG_STREAMING_INTERVAL = const(0x4)
JD_REG_READING = const(0x101)
JD_REG_MIN_READING = const(0x104)
JD_REG_MAX_READING = const(0x105)
JD_REG_READING_ERROR = const(0x106)
JD_REG_READING_RESOLUTION = const(0x108)
JD_REG_INACTIVE_THRESHOLD = const(0x5)
JD_REG_ACTIVE_THRESHOLD = const(0x6)
JD_REG_STREAMING_PREFERRED_INTERVAL = const(0x102)
JD_REG_VARIANT = const(0x107)
JD_REG_STATUS_CODE = const(0x103)
JD_REG_INSTANCE_NAME = const(0x109)
JD_EV_ACTIVE = const(0x1)
JD_EV_INACTIVE = const(0x2)
JD_EV_CHANGE = const(0x3)
JD_EV_STATUS_CODE_CHANGED = const(0x4)
JD_EV_NEUTRAL = const(0x7)

CMD_GET_REG = const(0x1000)
CMD_SET_REG = const(0x2000)
CMD_TYPE_MASK = const(0xf000)
CMD_REG_MASK = const(0x0fff)
CMD_EVENT_MASK = const(0x8000)
CMD_EVENT_CODE_MASK = const(0xff)
CMD_EVENT_COUNTER_MASK = const(0x7f)
CMD_EVENT_COUNTER_POS = const(8)

def JD_GET(code: int):
    assert 0 <= code and code <= 0xfff
    return CMD_GET_REG | code

def JD_SET(code: int):
    assert 0 <= code and code <= 0xfff
    return CMD_SET_REG | code
