# Autogenerated constants for DC Current Measurement service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_DC_CURRENT_MEASUREMENT = const(0x1912c8ae)
JD_DC_CURRENT_MEASUREMENT_REG_MEASUREMENT_NAME = const(0x182)
JD_DC_CURRENT_MEASUREMENT_REG_MEASUREMENT = const(JD_REG_READING)
JD_DC_CURRENT_MEASUREMENT_REG_MEASUREMENT_ERROR = const(JD_REG_READING_ERROR)
JD_DC_CURRENT_MEASUREMENT_REG_MIN_MEASUREMENT = const(JD_REG_MIN_READING)
JD_DC_CURRENT_MEASUREMENT_REG_MAX_MEASUREMENT = const(JD_REG_MAX_READING)
JD_DC_CURRENT_MEASUREMENT_PACK_FORMATS = {
    JD_DC_CURRENT_MEASUREMENT_REG_MEASUREMENT_NAME: "s",
    JD_DC_CURRENT_MEASUREMENT_REG_MEASUREMENT: "f64",
    JD_DC_CURRENT_MEASUREMENT_REG_MEASUREMENT_ERROR: "f64",
    JD_DC_CURRENT_MEASUREMENT_REG_MIN_MEASUREMENT: "f64",
    JD_DC_CURRENT_MEASUREMENT_REG_MAX_MEASUREMENT: "f64"
}
