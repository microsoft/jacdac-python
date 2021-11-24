
from ..bus import Bus
from .server import RngServer

if __name__ == '__main__':
    bus = Bus()

    rng = RngServer(bus)
