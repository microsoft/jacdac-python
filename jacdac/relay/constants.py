"""
Autogenerated constants for Relay service
"""
from enum import Enum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_RELAY = const(0x183fe656)
class RelayVariant(Enum):
    ELECTROMECHANICAL = const(0x1)
    SOLID_STATE = const(0x2)
    REED = const(0x3)

JD_RELAY_REG_CLOSED = const(JD_REG_INTENSITY)
JD_RELAY_REG_VARIANT = const(JD_REG_VARIANT)
JD_RELAY_REG_MAX_SWITCHING_CURRENT = const(0x180)
JD_RELAY_EV_ACTIVE = const(JD_EV_ACTIVE)
JD_RELAY_EV_INACTIVE = const(JD_EV_INACTIVE)
JD_RELAY_PACK_FORMATS = {
    JD_RELAY_REG_CLOSED: "u8",
    JD_RELAY_REG_VARIANT: "u8",
    JD_RELAY_REG_MAX_SWITCHING_CURRENT: "u32"
}
