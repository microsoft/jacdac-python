# Autogenerated constants for PC monitor service
from jacdac.constants import *
JD_SERVICE_CLASS_P_CMONITOR = const(0x18627b15)
JD_P_CMONITOR_REG_CPU_USAGE = const(0x190)
JD_P_CMONITOR_REG_CPU_TEMP = const(0x191)
JD_P_CMONITOR_REG_RAM_USAGE = const(0x192)
JD_P_CMONITOR_REG_GPU_INFO = const(0x193)
JD_P_CMONITOR_REG_NET_INFO = const(0x195)
JD_P_CMONITOR_PACK_FORMATS = {
    JD_P_CMONITOR_REG_CPU_USAGE: "u8",
    JD_P_CMONITOR_REG_CPU_TEMP: "u8",
    JD_P_CMONITOR_REG_RAM_USAGE: "u8",
    JD_P_CMONITOR_REG_GPU_INFO: "u8 u8",
    JD_P_CMONITOR_REG_NET_INFO: "u16 u16"
}