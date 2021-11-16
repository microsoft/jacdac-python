# Autogenerated constants for HID Adapter service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_HID_ADAPTER = const(0x1e5758b5)
JD_HID_ADAPTER_REG_NUM_CONFIGURATIONS = const(0x80)
JD_HID_ADAPTER_REG_CURRENT_CONFIGURATION = const(0x81)
JD_HID_ADAPTER_CMD_GET_CONFIGURATION = const(0x80)
JD_HID_ADAPTER_CMD_SET_BINDING = const(0x82)
JD_HID_ADAPTER_CMD_CLEAR_BINDING = const(0x83)
JD_HID_ADAPTER_CMD_CLEAR_CONFIGURATION = const(0x84)
JD_HID_ADAPTER_CMD_CLEAR = const(0x85)
JD_HID_ADAPTER_EV_CHANGED = const(JD_EV_CHANGE)