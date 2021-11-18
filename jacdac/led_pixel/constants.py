# Autogenerated constants for LED Pixel service
from enum import Enum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_LED_PIXEL = const(0x126f00e0)


class LedPixelLightType(Enum):
    WS2812B_GRB = const(0x0)
    APA102 = const(0x10)
    SK9822 = const(0x11)


class LedPixelVariant(Enum):
    STRIP = const(0x1)
    RING = const(0x2)
    STICK = const(0x3)
    JEWEL = const(0x4)
    MATRIX = const(0x5)


JD_LED_PIXEL_REG_BRIGHTNESS = const(JD_REG_INTENSITY)
JD_LED_PIXEL_REG_ACTUAL_BRIGHTNESS = const(0x180)
JD_LED_PIXEL_REG_LIGHT_TYPE = const(0x80)
JD_LED_PIXEL_REG_NUM_PIXELS = const(0x81)
JD_LED_PIXEL_REG_NUM_COLUMNS = const(0x83)
JD_LED_PIXEL_REG_MAX_POWER = const(JD_REG_MAX_POWER)
JD_LED_PIXEL_REG_MAX_PIXELS = const(0x181)
JD_LED_PIXEL_REG_NUM_REPEATS = const(0x82)
JD_LED_PIXEL_REG_VARIANT = const(JD_REG_VARIANT)
JD_LED_PIXEL_CMD_RUN = const(0x81)
JD_LED_PIXEL_PACK_FORMATS = {
    JD_LED_PIXEL_REG_BRIGHTNESS: "u0.8",
    JD_LED_PIXEL_REG_ACTUAL_BRIGHTNESS: "u0.8",
    JD_LED_PIXEL_REG_LIGHT_TYPE: "u8",
    JD_LED_PIXEL_REG_NUM_PIXELS: "u16",
    JD_LED_PIXEL_REG_NUM_COLUMNS: "u16",
    JD_LED_PIXEL_REG_MAX_POWER: "u16",
    JD_LED_PIXEL_REG_MAX_PIXELS: "u16",
    JD_LED_PIXEL_REG_NUM_REPEATS: "u16",
    JD_LED_PIXEL_REG_VARIANT: "u8",
    JD_LED_PIXEL_CMD_RUN: "b"
}
