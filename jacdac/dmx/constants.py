# Autogenerated constants for DMX service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_DMX = const(0x11cf8c05)
JD_DMX_REG_ENABLED = const(JD_REG_INTENSITY)
JD_DMX_CMD_SEND = const(0x80)
JD_DMX_PACK_FORMATS = {
    JD_DMX_REG_ENABLED: "u8",
    JD_DMX_CMD_SEND: "b"
}