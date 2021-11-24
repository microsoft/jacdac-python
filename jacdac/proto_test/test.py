from ..bus import Bus
#from .client import ProtoTestClient
from .server import ProtoTestServer

if __name__ == '__main__':
    bus = Bus()

    proto = ProtoTestServer(bus)
