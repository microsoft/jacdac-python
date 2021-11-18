# Autogenerated constants for Thermocouple service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_THERMOCOUPLE = const(0x143ac061)


class ThermocoupleVariant(IntEnum):
    TYPE_K = const(0x1)
    TYPE_J = const(0x2)
    TYPE_T = const(0x3)
    TYPE_E = const(0x4)
    TYPE_N = const(0x5)
    TYPE_S = const(0x6)
    TYPE_R = const(0x7)
    TYPE_B = const(0x8)


JD_THERMOCOUPLE_REG_TEMPERATURE = const(JD_REG_READING)
JD_THERMOCOUPLE_REG_MIN_TEMPERATURE = const(JD_REG_MIN_READING)
JD_THERMOCOUPLE_REG_MAX_TEMPERATURE = const(JD_REG_MAX_READING)
JD_THERMOCOUPLE_REG_TEMPERATURE_ERROR = const(JD_REG_READING_ERROR)
JD_THERMOCOUPLE_REG_VARIANT = const(JD_REG_VARIANT)
JD_THERMOCOUPLE_PACK_FORMATS = {
    JD_THERMOCOUPLE_REG_TEMPERATURE: "i22.10",
    JD_THERMOCOUPLE_REG_MIN_TEMPERATURE: "i22.10",
    JD_THERMOCOUPLE_REG_MAX_TEMPERATURE: "i22.10",
    JD_THERMOCOUPLE_REG_TEMPERATURE_ERROR: "u22.10",
    JD_THERMOCOUPLE_REG_VARIANT: "u8"
}
