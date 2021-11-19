from jacdac.devtools import create_dev_tools_bus
from .client import BarometerClient
from time import sleep

if __name__ == '__main__':
    bus = create_dev_tools_bus()

    barometer = BarometerClient(bus, "barometer")
    while True:
        print("pressure: ", barometer.pressure, "e:", barometer.pressure_error)
        sleep(1)
