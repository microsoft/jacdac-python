# Autogenerated constants for WIFI service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_WIFI = const(0x18aae1fa)


class WifiAPFlags(IntEnum):
    HAS_PASSWORD = const(0x1)
    WPS = const(0x2)
    HAS_SECONDARY_CHANNEL_ABOVE = const(0x4)
    HAS_SECONDARY_CHANNEL_BELOW = const(0x8)
    IEEE_802_11B = const(0x100)
    IEEE_802_11A = const(0x200)
    IEEE_802_11G = const(0x400)
    IEEE_802_11N = const(0x800)
    IEEE_802_11AC = const(0x1000)
    IEEE_802_11AX = const(0x2000)
    IEEE_802_LONG_RANGE = const(0x8000)


JD_WIFI_CMD_LAST_SCAN_RESULTS = const(0x80)
JD_WIFI_CMD_ADD_NETWORK = const(0x81)
JD_WIFI_CMD_RECONNECT = const(0x82)
JD_WIFI_CMD_FORGET_NETWORK = const(0x83)
JD_WIFI_CMD_FORGET_ALL_NETWORKS = const(0x84)
JD_WIFI_CMD_SET_NETWORK_PRIORITY = const(0x85)
JD_WIFI_CMD_SCAN = const(0x86)
JD_WIFI_CMD_LIST_KNOWN_NETWORKS = const(0x87)
JD_WIFI_REG_RSSI = const(JD_REG_READING)
JD_WIFI_REG_ENABLED = const(JD_REG_INTENSITY)
JD_WIFI_REG_IP_ADDRESS = const(0x181)
JD_WIFI_REG_EUI_48 = const(0x182)
JD_WIFI_REG_SSID = const(0x183)
JD_WIFI_EV_GOT_IP = const(JD_EV_ACTIVE)
JD_WIFI_EV_LOST_IP = const(JD_EV_INACTIVE)
JD_WIFI_EV_SCAN_COMPLETE = const(0x80)
JD_WIFI_EV_NETWORKS_CHANGED = const(0x81)
JD_WIFI_EV_CONNECTION_FAILED = const(0x82)
JD_WIFI_PACK_FORMATS = {
    JD_WIFI_CMD_LAST_SCAN_RESULTS: "b[12]",
    JD_WIFI_CMD_ADD_NETWORK: "z z",
    JD_WIFI_CMD_FORGET_NETWORK: "s",
    JD_WIFI_CMD_SET_NETWORK_PRIORITY: "i16 s",
    JD_WIFI_CMD_LIST_KNOWN_NETWORKS: "b[12]",
    JD_WIFI_REG_RSSI: "i8",
    JD_WIFI_REG_ENABLED: "u8",
    JD_WIFI_REG_IP_ADDRESS: "b[16]",
    JD_WIFI_REG_EUI_48: "b[6]",
    JD_WIFI_REG_SSID: "s[32]",
    JD_WIFI_EV_SCAN_COMPLETE: "u16 u16",
    JD_WIFI_EV_CONNECTION_FAILED: "s"
}
