# Autogenerated constants for Settings service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_SETTINGS = const(0x1107dc4a)
JD_SETTINGS_CMD_GET = const(0x80)
JD_SETTINGS_CMD_SET = const(0x81)
JD_SETTINGS_CMD_DELETE = const(0x84)
JD_SETTINGS_CMD_LIST_KEYS = const(0x82)
JD_SETTINGS_CMD_LIST = const(0x83)
JD_SETTINGS_CMD_CLEAR = const(0x85)
JD_SETTINGS_EV_CHANGE = const(JD_EV_CHANGE)
JD_SETTINGS_PACK_FORMATS = {
    JD_SETTINGS_CMD_GET: "s",
    JD_SETTINGS_CMD_SET: "z b",
    JD_SETTINGS_CMD_DELETE: "s",
    JD_SETTINGS_CMD_LIST_KEYS: "b[12]",
    JD_SETTINGS_CMD_LIST: "b[12]"
}