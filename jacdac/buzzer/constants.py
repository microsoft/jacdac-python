# Autogenerated constants for Buzzer service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_BUZZER = const(0x1b57b1d7)
JD_BUZZER_REG_VOLUME = const(JD_REG_INTENSITY)
JD_BUZZER_CMD_PLAY_TONE = const(0x80)
JD_BUZZER_CMD_PLAY_NOTE = const(0x81)
JD_BUZZER_PACK_FORMATS = {
    JD_BUZZER_REG_VOLUME: "u0.8",
    JD_BUZZER_CMD_PLAY_TONE: "u16 u16 u16",
    JD_BUZZER_CMD_PLAY_NOTE: "u16 u0.16 u16"
}
