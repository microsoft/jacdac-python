# Autogenerated constants for LED service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_LED = const(0x1e3048f8)
JD_LED_VARIANT_THROUGH_HOLE = const(0x1)
JD_LED_VARIANT_SMD = const(0x2)
JD_LED_VARIANT_POWER = const(0x3)
JD_LED_VARIANT_BEAD = const(0x4)
JD_LED_CMD_ANIMATE = const(0x80)
JD_LED_REG_COLOR = const(0x180)
JD_LED_REG_MAX_POWER = const(JD_REG_MAX_POWER)
JD_LED_REG_LED_COUNT = const(0x183)
JD_LED_REG_WAVE_LENGTH = const(0x181)
JD_LED_REG_LUMINOUS_INTENSITY = const(0x182)
JD_LED_REG_VARIANT = const(JD_REG_VARIANT)