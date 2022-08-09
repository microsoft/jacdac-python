# Autogenerated constants for Satellite Navigation System service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_SAT_NAV = const(0x19dd6136)
JD_SAT_NAV_REG_POSITION = const(JD_REG_READING)
JD_SAT_NAV_REG_ENABLED = const(JD_REG_INTENSITY)
JD_SAT_NAV_EV_INACTIVE = const(JD_EV_INACTIVE)
JD_SAT_NAV_PACK_FORMATS = {
    JD_SAT_NAV_REG_POSITION: "u64 i9.23 i9.23 u16.16 i26.6 u16.16",
    JD_SAT_NAV_REG_ENABLED: "u8"
}