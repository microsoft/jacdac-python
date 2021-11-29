from ..bus import Bus
from ..relay.client import RelayClient
from ..led.client import LedClient
from time import sleep

if __name__ == '__main__':
    bus = Bus()

    rel = RelayClient(bus, "relay")
    rel2 = RelayClient(bus, "relay2")
    led = LedClient(bus, "led")
    led2 = LedClient(bus, "led2")
    leda = LedClient(bus, "device/leda")
    ledb = LedClient(bus, "device/ledb")
    ledc = LedClient(bus, "device/ledc")
    led2a = LedClient(bus, "device2/leda")
    led2b = LedClient(bus, "device2/ledb")
    led2c = LedClient(bus, "device2/ledc")
    led2d = LedClient(bus, "device2/ledd")

    while True:
        sleep(1)
