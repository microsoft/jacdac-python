# Autogenerated constants for Potentiometer service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_POTENTIOMETER = const(0x1f274746)


class PotentiometerVariant(IntEnum):
    SLIDER = const(0x1)
    ROTARY = const(0x2)
    HALL = const(0x3)


JD_POTENTIOMETER_REG_POSITION = const(JD_REG_READING)
JD_POTENTIOMETER_REG_VARIANT = const(JD_REG_VARIANT)
JD_POTENTIOMETER_PACK_FORMATS = {
    JD_POTENTIOMETER_REG_POSITION: "u0.16",
    JD_POTENTIOMETER_REG_VARIANT: "u8"
}
