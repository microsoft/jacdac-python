# Autogenerated constants for Planar position service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_PLANAR_POSITION = const(0x1dc37f55)


class PlanarPositionVariant(IntEnum):
    OPTICAL_MOUSE_POSITION = const(0x1)


JD_PLANAR_POSITION_REG_POSITION = const(JD_REG_READING)
JD_PLANAR_POSITION_REG_VARIANT = const(JD_REG_VARIANT)
JD_PLANAR_POSITION_PACK_FORMATS = {
    JD_PLANAR_POSITION_REG_POSITION: "i22.10 i22.10",
    JD_PLANAR_POSITION_REG_VARIANT: "u8"
}
