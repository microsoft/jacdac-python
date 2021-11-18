# Autogenerated constants for Arcade Sound service
from jacdac.constants import *
JD_SERVICE_CLASS_ARCADE_SOUND = const(0x1fc63606)
JD_ARCADE_SOUND_CMD_PLAY = const(0x80)
JD_ARCADE_SOUND_REG_SAMPLE_RATE = const(0x80)
JD_ARCADE_SOUND_REG_BUFFER_SIZE = const(0x180)
JD_ARCADE_SOUND_REG_BUFFER_PENDING = const(0x181)
JD_ARCADE_SOUND_PACK_FORMATS = {
    JD_ARCADE_SOUND_CMD_PLAY: "b",
    JD_ARCADE_SOUND_REG_SAMPLE_RATE: "u22.10",
    JD_ARCADE_SOUND_REG_BUFFER_SIZE: "u32",
    JD_ARCADE_SOUND_REG_BUFFER_PENDING: "u32"
}
