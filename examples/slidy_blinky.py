from jacdac.devtools import create_dev_tools_bus
from jacdac.led import LedClient
from jacdac.potentiometer import PotentiometerClient
from time import sleep

if __name__ == '__main__':
    def main():
        bus = create_dev_tools_bus()
        led = LedClient(bus, "led")
        slider = PotentiometerClient(bus, "slider")
        speed = 16
        brightness = 128
        # fade between colors
        while True:
            position = slider.position or 0.
            brightness = int(position / 100. * 255.)
            # blue
            led.animate(0, 0, brightness, speed)
            sleep(1)
            # off
            led.animate(brightness, 0, 0, speed)
            sleep(1)

    main()
