# Autogenerated constants for Indexed screen service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_INDEXED_SCREEN = const(0x16fa36e5)
JD_INDEXED_SCREEN_CMD_START_UPDATE = const(0x81)
JD_INDEXED_SCREEN_CMD_SET_PIXELS = const(0x83)
JD_INDEXED_SCREEN_REG_BRIGHTNESS = const(JD_REG_INTENSITY)
JD_INDEXED_SCREEN_REG_PALETTE = const(0x80)
JD_INDEXED_SCREEN_REG_BITS_PER_PIXEL = const(0x180)
JD_INDEXED_SCREEN_REG_WIDTH = const(0x181)
JD_INDEXED_SCREEN_REG_HEIGHT = const(0x182)
JD_INDEXED_SCREEN_REG_WIDTH_MAJOR = const(0x81)
JD_INDEXED_SCREEN_REG_UP_SAMPLING = const(0x82)
JD_INDEXED_SCREEN_REG_ROTATION = const(0x83)
JD_INDEXED_SCREEN_PACK_FORMATS = {
    JD_INDEXED_SCREEN_CMD_START_UPDATE: "u16 u16 u16 u16",
    JD_INDEXED_SCREEN_CMD_SET_PIXELS: "b",
    JD_INDEXED_SCREEN_REG_BRIGHTNESS: "u0.8",
    JD_INDEXED_SCREEN_REG_PALETTE: "b",
    JD_INDEXED_SCREEN_REG_BITS_PER_PIXEL: "u8",
    JD_INDEXED_SCREEN_REG_WIDTH: "u16",
    JD_INDEXED_SCREEN_REG_HEIGHT: "u16",
    JD_INDEXED_SCREEN_REG_WIDTH_MAJOR: "u8",
    JD_INDEXED_SCREEN_REG_UP_SAMPLING: "u8",
    JD_INDEXED_SCREEN_REG_ROTATION: "u16"
}
