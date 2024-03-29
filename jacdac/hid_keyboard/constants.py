# Autogenerated constants for HID Keyboard service
from enum import IntEnum
from jacdac.constants import *
JD_SERVICE_CLASS_HID_KEYBOARD = const(0x18b05b6a)


class HidKeyboardSelector(IntEnum):
    NONE = const(0x0)
    ERROR_ROLL_OVER = const(0x1)
    POST_FAIL = const(0x2)
    ERROR_UNDEFINED = const(0x3)
    A = const(0x4)
    B = const(0x5)
    C = const(0x6)
    D = const(0x7)
    E = const(0x8)
    F = const(0x9)
    G = const(0xa)
    H = const(0xb)
    I = const(0xc)
    J = const(0xd)
    K = const(0xe)
    L = const(0xf)
    M = const(0x10)
    N = const(0x11)
    O = const(0x12)
    P = const(0x13)
    Q = const(0x14)
    R = const(0x15)
    S = const(0x16)
    T = const(0x17)
    U = const(0x18)
    V = const(0x19)
    W = const(0x1a)
    X = const(0x1b)
    Y = const(0x1c)
    Z = const(0x1d)
    _1 = const(0x1e)
    _2 = const(0x1f)
    _3 = const(0x20)
    _4 = const(0x21)
    _5 = const(0x22)
    _6 = const(0x23)
    _7 = const(0x24)
    _8 = const(0x25)
    _9 = const(0x26)
    _0 = const(0x27)
    RETURN = const(0x28)
    ESCAPE = const(0x29)
    BACKSPACE = const(0x2a)
    TAB = const(0x2b)
    SPACEBAR = const(0x2c)
    MINUS = const(0x2d)
    EQUALS = const(0x2e)
    LEFT_SQUARE_BRACKET = const(0x2f)
    RIGHT_SQUARE_BRACKET = const(0x30)
    BACKSLASH = const(0x31)
    NON_US_HASH = const(0x32)
    SEMICOLON = const(0x33)
    QUOTE = const(0x34)
    GRAVE_ACCENT = const(0x35)
    COMMA = const(0x36)
    PERIOD = const(0x37)
    SLASH = const(0x38)
    CAPS_LOCK = const(0x39)
    F1 = const(0x3a)
    F2 = const(0x3b)
    F3 = const(0x3c)
    F4 = const(0x3d)
    F5 = const(0x3e)
    F6 = const(0x3f)
    F7 = const(0x40)
    F8 = const(0x41)
    F9 = const(0x42)
    F10 = const(0x43)
    F11 = const(0x44)
    F12 = const(0x45)
    PRINT_SCREEN = const(0x46)
    SCROLL_LOCK = const(0x47)
    PAUSE = const(0x48)
    INSERT = const(0x49)
    HOME = const(0x4a)
    PAGE_UP = const(0x4b)
    DELETE = const(0x4c)
    END = const(0x4d)
    PAGE_DOWN = const(0x4e)
    RIGHT_ARROW = const(0x4f)
    LEFT_ARROW = const(0x50)
    DOWN_ARROW = const(0x51)
    UP_ARROW = const(0x52)
    KEYPAD_NUM_LOCK = const(0x53)
    KEYPAD_DIVIDE = const(0x54)
    KEYPAD_MULTIPLY = const(0x55)
    KEYPAD_ADD = const(0x56)
    KEYPAD_SUBTRACE = const(0x57)
    KEYPAD_RETURN = const(0x58)
    KEYPAD1 = const(0x59)
    KEYPAD2 = const(0x5a)
    KEYPAD3 = const(0x5b)
    KEYPAD4 = const(0x5c)
    KEYPAD5 = const(0x5d)
    KEYPAD6 = const(0x5e)
    KEYPAD7 = const(0x5f)
    KEYPAD8 = const(0x60)
    KEYPAD9 = const(0x61)
    KEYPAD0 = const(0x62)
    KEYPAD_DECIMAL_POINT = const(0x63)
    NON_US_BACKSLASH = const(0x64)
    APPLICATION = const(0x65)
    POWER = const(0x66)
    KEYPAD_EQUALS = const(0x67)
    F13 = const(0x68)
    F14 = const(0x69)
    F15 = const(0x6a)
    F16 = const(0x6b)
    F17 = const(0x6c)
    F18 = const(0x6d)
    F19 = const(0x6e)
    F20 = const(0x6f)
    F21 = const(0x70)
    F22 = const(0x71)
    F23 = const(0x72)
    F24 = const(0x73)
    EXECUTE = const(0x74)
    HELP = const(0x75)
    MENU = const(0x76)
    SELECT = const(0x77)
    STOP = const(0x78)
    AGAIN = const(0x79)
    UNDO = const(0x7a)
    CUT = const(0x7b)
    COPY = const(0x7c)
    PASTE = const(0x7d)
    FIND = const(0x7e)
    MUTE = const(0x7f)
    VOLUME_UP = const(0x80)
    VOLUME_DOWN = const(0x81)


class HidKeyboardModifiers(IntEnum):
    NONE = const(0x0)
    LEFT_CONTROL = const(0x1)
    LEFT_SHIFT = const(0x2)
    LEFT_ALT = const(0x4)
    LEFT_GUI = const(0x8)
    RIGHT_CONTROL = const(0x10)
    RIGHT_SHIFT = const(0x20)
    RIGHT_ALT = const(0x40)
    RIGHT_GUI = const(0x80)


class HidKeyboardAction(IntEnum):
    PRESS = const(0x0)
    UP = const(0x1)
    DOWN = const(0x2)


JD_HID_KEYBOARD_CMD_KEY = const(0x80)
JD_HID_KEYBOARD_CMD_CLEAR = const(0x81)
JD_HID_KEYBOARD_PACK_FORMATS = {
    JD_HID_KEYBOARD_CMD_KEY: "r: u16 u8 u8"
}
