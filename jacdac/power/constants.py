# Autogenerated constants for Power service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_POWER = const(0x1fa4c95a)
JD_POWER_POWER_STATUS_DISALLOWED = const(0x0)
JD_POWER_POWER_STATUS_POWERING = const(0x1)
JD_POWER_POWER_STATUS_OVERLOAD = const(0x2)
JD_POWER_POWER_STATUS_OVERPROVISION = const(0x3)
JD_POWER_REG_ALLOWED = const(JD_REG_INTENSITY)
JD_POWER_REG_MAX_POWER = const(JD_REG_MAX_POWER)
JD_POWER_REG_POWER_STATUS = const(0x181)
JD_POWER_REG_CURRENT_DRAW = const(JD_REG_READING)
JD_POWER_REG_BATTERY_VOLTAGE = const(0x180)
JD_POWER_REG_BATTERY_CHARGE = const(0x182)
JD_POWER_REG_BATTERY_CAPACITY = const(0x183)
JD_POWER_REG_KEEP_ON_PULSE_DURATION = const(0x80)
JD_POWER_REG_KEEP_ON_PULSE_PERIOD = const(0x81)
JD_POWER_CMD_SHUTDOWN = const(0x80)
JD_POWER_EV_POWER_STATUS_CHANGED = const(JD_EV_CHANGE)