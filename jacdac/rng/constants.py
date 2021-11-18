# Autogenerated constants for Random Number Generator service
from enum import Enum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_RNG = const(0x1789f0a2)


class RngVariant(Enum):
    QUANTUM = const(0x1)
    ADCNOISE = const(0x2)
    WEB_CRYPTO = const(0x3)


JD_RNG_REG_RANDOM = const(0x180)
JD_RNG_REG_VARIANT = const(JD_REG_VARIANT)
JD_RNG_PACK_FORMATS = {
    JD_RNG_REG_RANDOM: "b",
    JD_RNG_REG_VARIANT: "u8"
}
