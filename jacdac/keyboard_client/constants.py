# Autogenerated constants for Keyboard client service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_KEYBOARD_CLIENT = const(0x113d023e)
JD_KEYBOARD_CLIENT_EV_DOWN = const(JD_EV_ACTIVE)
JD_KEYBOARD_CLIENT_EV_HOLD = const(0x81)
JD_KEYBOARD_CLIENT_PACK_FORMATS = {
    JD_KEYBOARD_CLIENT_EV_DOWN: "u16",
    JD_KEYBOARD_CLIENT_EV_HOLD: "u16"
}