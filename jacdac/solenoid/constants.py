# Autogenerated constants for Solenoid service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_SOLENOID = const(0x171723ca)


class SolenoidVariant(IntEnum):
    PUSH_PULL = const(0x1)
    VALVE = const(0x2)
    LATCH = const(0x3)


JD_SOLENOID_REG_PULLED = const(JD_REG_INTENSITY)
JD_SOLENOID_REG_VARIANT = const(JD_REG_VARIANT)
JD_SOLENOID_PACK_FORMATS = {
    JD_SOLENOID_REG_PULLED: "u8",
    JD_SOLENOID_REG_VARIANT: "u8"
}
