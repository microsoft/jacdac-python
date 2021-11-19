from jacdac.devtools import create_dev_tools_bus
from .client import ThermometerClient
from time import sleep

if __name__ == '__main__':
    bus = create_dev_tools_bus()

    client = ThermometerClient(bus, "client")
    while True:
        print("temp: ", client.temperature, "error:", client.temperature_error)
        sleep(0.2)
