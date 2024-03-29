# Autogenerated constants for Sound level service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_SOUND_LEVEL = const(0x14ad1a5d)
JD_SOUND_LEVEL_REG_SOUND_LEVEL = const(JD_REG_READING)
JD_SOUND_LEVEL_REG_ENABLED = const(JD_REG_INTENSITY)
JD_SOUND_LEVEL_REG_LOUD_THRESHOLD = const(JD_REG_ACTIVE_THRESHOLD)
JD_SOUND_LEVEL_REG_QUIET_THRESHOLD = const(JD_REG_INACTIVE_THRESHOLD)
JD_SOUND_LEVEL_EV_LOUD = const(JD_EV_ACTIVE)
JD_SOUND_LEVEL_EV_QUIET = const(JD_EV_INACTIVE)
JD_SOUND_LEVEL_PACK_FORMATS = {
    JD_SOUND_LEVEL_REG_SOUND_LEVEL: "u0.16",
    JD_SOUND_LEVEL_REG_ENABLED: "u8",
    JD_SOUND_LEVEL_REG_LOUD_THRESHOLD: "u0.16",
    JD_SOUND_LEVEL_REG_QUIET_THRESHOLD: "u0.16"
}
