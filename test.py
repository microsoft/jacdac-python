import sys
from jacdac.bus import Bus

if __name__ == '__main__':
    bus = Bus(hf2_portname=sys.argv[1])
