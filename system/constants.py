# Autogenerated constants for Common registers and commands service
from jacdac.constants import *
JD_ANNOUNCE_INTERVAL = const(0x1f4)

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
JD_CMD_GET_REGISTER = const(0x1000)
JD_CMD_SET_REGISTER = const(0x2000)
JD_CMD_EVENT = const(0x1)
JD_CMD_CALIBRATE = const(0x2)
JD_CMD_COMMAND_NOT_IMPLEMENTED = const(0x3)
JD_REG_INTENSITY = const(0x1)
JD_REG_VALUE = const(0x2)
JD_REG_MIN_VALUE = const(0x110)
JD_REG_MAX_VALUE = const(0x111)
JD_REG_MAX_POWER = const(0x7)
JD_REG_STREAMING_SAMPLES = const(0x3)
JD_REG_STREAMING_INTERVAL = const(0x4)
JD_REG_READING = const(0x101)
JD_REG_READING_RANGE = const(0x8)
JD_REG_SUPPORTED_RANGES = const(0x10a)
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