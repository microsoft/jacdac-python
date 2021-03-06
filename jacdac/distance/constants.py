# Autogenerated constants for Distance service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_DISTANCE = const(0x141a6b8a)


class DistanceVariant(IntEnum):
    ULTRASONIC = const(0x1)
    INFRARED = const(0x2)
    LI_DAR = const(0x3)
    LASER = const(0x4)


JD_DISTANCE_REG_DISTANCE = const(JD_REG_READING)
JD_DISTANCE_REG_DISTANCE_ERROR = const(JD_REG_READING_ERROR)
JD_DISTANCE_REG_MIN_RANGE = const(JD_REG_MIN_READING)
JD_DISTANCE_REG_MAX_RANGE = const(JD_REG_MAX_READING)
JD_DISTANCE_REG_VARIANT = const(JD_REG_VARIANT)
JD_DISTANCE_PACK_FORMATS = {
    JD_DISTANCE_REG_DISTANCE: "u16.16",
    JD_DISTANCE_REG_DISTANCE_ERROR: "u16.16",
    JD_DISTANCE_REG_MIN_RANGE: "u16.16",
    JD_DISTANCE_REG_MAX_RANGE: "u16.16",
    JD_DISTANCE_REG_VARIANT: "u8"
}
