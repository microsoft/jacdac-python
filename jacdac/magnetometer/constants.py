# Autogenerated constants for Magnetometer service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_MAGNETOMETER = const(0x13029088)
JD_MAGNETOMETER_REG_FORCES = const(JD_REG_READING)
JD_MAGNETOMETER_REG_FORCES_ERROR = const(JD_REG_READING_ERROR)
JD_MAGNETOMETER_CMD_CALIBRATE = const(JD_CMD_CALIBRATE)
JD_MAGNETOMETER_PACK_FORMATS = {
    JD_MAGNETOMETER_REG_FORCES: "i32 i32 i32",
    JD_MAGNETOMETER_REG_FORCES_ERROR: "i32"
}
