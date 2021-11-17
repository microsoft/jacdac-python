"""
Autogenerated constants for Soil moisture service
"""
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_SOIL_MOISTURE = const(0x1d4aa3b3)
JD_SOIL_MOISTURE_VARIANT_RESISTIVE = const(0x1)
JD_SOIL_MOISTURE_VARIANT_CAPACITIVE = const(0x2)
JD_SOIL_MOISTURE_REG_MOISTURE = const(JD_REG_READING)
JD_SOIL_MOISTURE_REG_MOISTURE_ERROR = const(JD_REG_READING_ERROR)
JD_SOIL_MOISTURE_REG_VARIANT = const(JD_REG_VARIANT)
JD_SOIL_MOISTURE_PACK_FORMATS = {
    JD_SOIL_MOISTURE_REG_MOISTURE: "u0.16",
    JD_SOIL_MOISTURE_REG_MOISTURE_ERROR: "u0.16",
    JD_SOIL_MOISTURE_REG_VARIANT: "u8"
}
