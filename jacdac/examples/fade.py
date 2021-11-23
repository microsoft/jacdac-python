from jacdac.devtools import create_dev_tools_bus
from jacdac.led import LedClient
from time import sleep

if __name__ == '__main__':
    def main():
        bus = create_dev_tools_bus()
        led = LedClient(bus, "led")
        speed = 16
        brightness = 128
        # fade between colors
        while True:
            # blue
            led.animate(0, 0, brightness, speed)
            sleep(1)
            # red
            led.animate(brightness, 0, 0, speed)
            sleep(1)
            # green
            led.animate(0, brightness, 0, speed)
            sleep(1)

    main()
