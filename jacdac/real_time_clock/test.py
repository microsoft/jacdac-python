from ..bus import Bus
from .server import RealTimeClockServer
from time import sleep, localtime

if __name__ == '__main__':
    bus = Bus()

    clock = RealTimeClockServer(bus)
    while True:
        print(localtime())
        sleep(5)
