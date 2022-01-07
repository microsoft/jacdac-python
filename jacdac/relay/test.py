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
        rel.active = False
        sleep(1)
        print("open: ", rel.active)
        rel.active = True
        sleep(1)
        print("closed: ", rel.active)
