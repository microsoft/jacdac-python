from jacdac.devtools import create_dev_tools_bus
#from .client import ProtoTestClient
from .server import ProtoTestServer

if __name__ == '__main__':
    bus = create_dev_tools_bus()

    proto = ProtoTestServer(bus)
