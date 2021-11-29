from ..bus import Bus
from ..relay.client import RelayClient
from ..led.client import LedClient
from time import sleep

if __name__ == '__main__':
    bus = Bus()

    rel = RelayClient(bus, "relay")
    rel2 = RelayClient(bus, "relay2")
    led = LedClient(bus, "led")
    leda = LedClient(bus, "device/leda")
    ledb = LedClient(bus, "device/ledb")

    while True:
        sleep(1)
