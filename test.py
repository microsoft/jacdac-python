import sys
from jacdac.bus import Bus

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        bus = Bus(hf2_portname=sys.argv[1])
    else:
        bus = Bus()
