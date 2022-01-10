# Autogenerated constants for Gamepad service
from enum import IntEnum
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_GAMEPAD = const(0x108f7456)


class GamepadButtons(IntEnum):
    LEFT = const(0x1)
    UP = const(0x2)
    RIGHT = const(0x4)
    DOWN = const(0x8)
    A = const(0x10)
    B = const(0x20)
    MENU = const(0x40)
    SELECT = const(0x80)
    RESET = const(0x100)
    EXIT = const(0x200)
    X = const(0x400)
    Y = const(0x800)


class GamepadVariant(IntEnum):
    THUMB = const(0x1)
    ARCADE_BALL = const(0x2)
    ARCADE_STICK = const(0x3)
    GAMEPAD = const(0x4)


JD_GAMEPAD_REG_DIRECTION = const(JD_REG_READING)
JD_GAMEPAD_REG_VARIANT = const(JD_REG_VARIANT)
JD_GAMEPAD_REG_BUTTONS_AVAILABLE = const(0x180)
JD_GAMEPAD_EV_BUTTONS_CHANGED = const(JD_EV_CHANGE)
JD_GAMEPAD_PACK_FORMATS = {
    JD_GAMEPAD_REG_DIRECTION: "u32 i1.15 i1.15",
    JD_GAMEPAD_REG_VARIANT: "u8",
    JD_GAMEPAD_REG_BUTTONS_AVAILABLE: "u32",
    JD_GAMEPAD_EV_BUTTONS_CHANGED: "u32"
}