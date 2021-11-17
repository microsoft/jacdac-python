# Autogenerated constants for Model Runner service
from jacdac.constants import *
from jacdac.system.constants import *
JD_SERVICE_CLASS_MODEL_RUNNER = const(0x140f9a78)
JD_MODEL_RUNNER_MODEL_FORMAT_TFLITE = const(0x334c4654)
JD_MODEL_RUNNER_MODEL_FORMAT_ML4F = const(0x30470f62)
JD_MODEL_RUNNER_MODEL_FORMAT_EDGE_IMPULSE_COMPILED = const(0x30564945)
JD_MODEL_RUNNER_CMD_SET_MODEL = const(0x80)
JD_MODEL_RUNNER_CMD_PREDICT = const(0x81)
JD_MODEL_RUNNER_REG_AUTO_INVOKE_EVERY = const(0x80)
JD_MODEL_RUNNER_REG_OUTPUTS = const(JD_REG_READING)
JD_MODEL_RUNNER_REG_INPUT_SHAPE = const(0x180)
JD_MODEL_RUNNER_REG_OUTPUT_SHAPE = const(0x181)
JD_MODEL_RUNNER_REG_LAST_RUN_TIME = const(0x182)
JD_MODEL_RUNNER_REG_ALLOCATED_ARENA_SIZE = const(0x183)
JD_MODEL_RUNNER_REG_MODEL_SIZE = const(0x184)
JD_MODEL_RUNNER_REG_LAST_ERROR = const(0x185)
JD_MODEL_RUNNER_REG_FORMAT = const(0x186)
JD_MODEL_RUNNER_REG_FORMAT_VERSION = const(0x187)
JD_MODEL_RUNNER_REG_PARALLEL = const(0x188)
JD_MODEL_RUNNER_PACK_FORMATS = {
    JD_MODEL_RUNNER_CMD_SET_MODEL: "u32",
    JD_MODEL_RUNNER_CMD_PREDICT: "b[12]",
    JD_MODEL_RUNNER_REG_AUTO_INVOKE_EVERY: "u16",
    JD_MODEL_RUNNER_REG_OUTPUTS: "r: f32",
    JD_MODEL_RUNNER_REG_INPUT_SHAPE: "r: u16",
    JD_MODEL_RUNNER_REG_OUTPUT_SHAPE: "r: u16",
    JD_MODEL_RUNNER_REG_LAST_RUN_TIME: "u32",
    JD_MODEL_RUNNER_REG_ALLOCATED_ARENA_SIZE: "u32",
    JD_MODEL_RUNNER_REG_MODEL_SIZE: "u32",
    JD_MODEL_RUNNER_REG_LAST_ERROR: "s",
    JD_MODEL_RUNNER_REG_FORMAT: "u32",
    JD_MODEL_RUNNER_REG_FORMAT_VERSION: "u32",
    JD_MODEL_RUNNER_REG_PARALLEL: "u8"
}