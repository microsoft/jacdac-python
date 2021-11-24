from ..bus import Bus
from .client import ThermometerClient
from time import sleep

if __name__ == '__main__':
    bus = Bus()

    client = ThermometerClient(bus, "thermometer")
    while True:
        print("temp: ", client.temperature, "error:", client.temperature_error)
        sleep(0.2)
