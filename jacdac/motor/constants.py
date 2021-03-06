# Autogenerated constants for Motor service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_MOTOR = const(0x17004cd8)
JD_MOTOR_REG_SPEED = const(JD_REG_VALUE)
JD_MOTOR_REG_ENABLED = const(JD_REG_INTENSITY)
JD_MOTOR_REG_LOAD_TORQUE = const(0x180)
JD_MOTOR_REG_LOAD_ROTATION_SPEED = const(0x181)
JD_MOTOR_REG_REVERSIBLE = const(0x182)
JD_MOTOR_PACK_FORMATS = {
    JD_MOTOR_REG_SPEED: "i1.15",
    JD_MOTOR_REG_ENABLED: "u8",
    JD_MOTOR_REG_LOAD_TORQUE: "u16.16",
    JD_MOTOR_REG_LOAD_ROTATION_SPEED: "u16.16",
    JD_MOTOR_REG_REVERSIBLE: "u8"
}
