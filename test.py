import sys
import jacdac
from jacdac.transports.hf2 import HF2Transport

bus = jacdac.Bus(HF2Transport(sys.argv[1]))
