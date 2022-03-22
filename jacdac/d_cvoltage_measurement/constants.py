# Autogenerated constants for DC Voltage Measurement service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_D_CVOLTAGE_MEASUREMENT = const(0x1633ac19)


class DCVoltageMeasurementVoltageMeasurementType(IntEnum):
    ABSOLUTE = const(0x0)
    DIFFERENTIAL = const(0x1)


JD_D_CVOLTAGE_MEASUREMENT_REG_MEASUREMENT_TYPE = const(0x181)
JD_D_CVOLTAGE_MEASUREMENT_REG_MEASUREMENT_NAME = const(0x182)
JD_D_CVOLTAGE_MEASUREMENT_REG_MEASUREMENT = const(JD_REG_READING)
JD_D_CVOLTAGE_MEASUREMENT_PACK_FORMATS = {
    JD_D_CVOLTAGE_MEASUREMENT_REG_MEASUREMENT_TYPE: "u8",
    JD_D_CVOLTAGE_MEASUREMENT_REG_MEASUREMENT_NAME: "s",
    JD_D_CVOLTAGE_MEASUREMENT_REG_MEASUREMENT: "f64"
}
