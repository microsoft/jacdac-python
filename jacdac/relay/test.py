from typing import Any
from ..bus import Bus
from .client import RelayClient
from time import sleep

if __name__ == '__main__':
    bus = Bus()

    def active(data: Any):
        print("active")

    def inactive(data: Any):
        print("inactive")

    rel = RelayClient(bus, "relay")

    while True:
        rel.closed = False
        sleep(1)
        print("open: ", rel.closed)
        rel.closed = True
        sleep(1)
        print("closed: ", rel.closed)
