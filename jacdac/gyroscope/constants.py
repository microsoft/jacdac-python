"""
Autogenerated constants for Gyroscope service
"""
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_GYROSCOPE = const(0x1e1b06f2)
JD_GYROSCOPE_REG_ROTATION_RATES = const(JD_REG_READING)
JD_GYROSCOPE_REG_ROTATION_RATES_ERROR = const(JD_REG_READING_ERROR)
JD_GYROSCOPE_REG_MAX_RATE = const(JD_REG_READING_RANGE)
JD_GYROSCOPE_REG_MAX_RATES_SUPPORTED = const(JD_REG_SUPPORTED_RANGES)
JD_GYROSCOPE_PACK_FORMATS = {
    JD_GYROSCOPE_REG_ROTATION_RATES: "i12.20 i12.20 i12.20",
    JD_GYROSCOPE_REG_ROTATION_RATES_ERROR: "u12.20",
    JD_GYROSCOPE_REG_MAX_RATE: "u12.20",
    JD_GYROSCOPE_REG_MAX_RATES_SUPPORTED: "r: u12.20"
}
