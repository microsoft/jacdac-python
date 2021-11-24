from ..bus import Bus
from .client import BarometerClient
from time import sleep

if __name__ == '__main__':
    bus = Bus()

    barometer = BarometerClient(bus, "barometer")
    while True:
        print("pressure: ", barometer.pressure, "e:", barometer.pressure_error)
        sleep(1)
