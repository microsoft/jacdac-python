# Autogenerated constants for LED Display service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_LED_DISPLAY = const(0x1609d4f0)
JD_MAX_PIXELS_LENGTH = const(0x40)



class LedDisplayLightType(IntEnum):
    WS2812B_GRB = const(0x0)
    APA102 = const(0x10)
    SK9822 = const(0x11)


class LedDisplayVariant(IntEnum):
    STRIP = const(0x1)
    RING = const(0x2)
    STICK = const(0x3)
    JEWEL = const(0x4)
    MATRIX = const(0x5)


JD_LED_DISPLAY_REG_PIXELS = const(JD_REG_VALUE)
JD_LED_DISPLAY_REG_BRIGHTNESS = const(JD_REG_INTENSITY)
JD_LED_DISPLAY_REG_ACTUAL_BRIGHTNESS = const(0x180)
JD_LED_DISPLAY_REG_LIGHT_TYPE = const(0x181)
JD_LED_DISPLAY_REG_NUM_PIXELS = const(0x182)
JD_LED_DISPLAY_REG_NUM_COLUMNS = const(0x183)
JD_LED_DISPLAY_REG_MAX_POWER = const(JD_REG_MAX_POWER)
JD_LED_DISPLAY_REG_VARIANT = const(JD_REG_VARIANT)
JD_LED_DISPLAY_PACK_FORMATS = {
    JD_LED_DISPLAY_REG_PIXELS: "b",
    JD_LED_DISPLAY_REG_BRIGHTNESS: "u0.8",
    JD_LED_DISPLAY_REG_ACTUAL_BRIGHTNESS: "u0.8",
    JD_LED_DISPLAY_REG_LIGHT_TYPE: "u8",
    JD_LED_DISPLAY_REG_NUM_PIXELS: "u16",
    JD_LED_DISPLAY_REG_NUM_COLUMNS: "u16",
    JD_LED_DISPLAY_REG_MAX_POWER: "u16",
    JD_LED_DISPLAY_REG_VARIANT: "u8"
}
