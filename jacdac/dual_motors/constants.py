# Autogenerated constants for Dual Motors service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_DUAL_MOTORS = const(0x1529d537)
JD_DUAL_MOTORS_REG_SPEED = const(JD_REG_VALUE)
JD_DUAL_MOTORS_REG_ENABLED = const(JD_REG_INTENSITY)
JD_DUAL_MOTORS_REG_LOAD_TORQUE = const(0x180)
JD_DUAL_MOTORS_REG_LOAD_ROTATION_SPEED = const(0x181)
JD_DUAL_MOTORS_REG_REVERSIBLE = const(0x182)
JD_DUAL_MOTORS_PACK_FORMATS = {
    JD_DUAL_MOTORS_REG_SPEED: "i1.15 i1.15",
    JD_DUAL_MOTORS_REG_ENABLED: "u8",
    JD_DUAL_MOTORS_REG_LOAD_TORQUE: "u16.16",
    JD_DUAL_MOTORS_REG_LOAD_ROTATION_SPEED: "u16.16",
    JD_DUAL_MOTORS_REG_REVERSIBLE: "u8"
}
