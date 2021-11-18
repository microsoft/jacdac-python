import sys
from jacdac.bus import Bus
from jacdac.transports.hf2 import HF2Transport

if __name__ == '__main__':
    bus = Bus(HF2Transport(sys.argv[1]))
