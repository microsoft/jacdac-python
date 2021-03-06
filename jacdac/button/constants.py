# Autogenerated constants for Button service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_BUTTON = const(0x1473a263)
JD_BUTTON_REG_PRESSURE = const(JD_REG_READING)
JD_BUTTON_REG_ANALOG = const(0x180)
JD_BUTTON_REG_PRESSED = const(0x181)
JD_BUTTON_EV_DOWN = const(JD_EV_ACTIVE)
JD_BUTTON_EV_UP = const(JD_EV_INACTIVE)
JD_BUTTON_EV_HOLD = const(0x81)
JD_BUTTON_PACK_FORMATS = {
    JD_BUTTON_REG_PRESSURE: "u0.16",
    JD_BUTTON_REG_ANALOG: "u8",
    JD_BUTTON_REG_PRESSED: "u8",
    JD_BUTTON_EV_UP: "u32",
    JD_BUTTON_EV_HOLD: "u32"
}
