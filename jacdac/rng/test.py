
from jacdac.devtools import create_dev_tools_bus
from .server import RngServer

if __name__ == '__main__':
    bus = create_dev_tools_bus(
        device_description='rng server test')

    rng = RngServer(bus)