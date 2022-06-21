from jacdac import Bus
from jacdac.led import LedClient
from time import sleep

if __name__ == '__main__':
    def main():
        bus = Bus()
        led = LedClient(bus, "led")
        led.brightness = 0.5
        # fade between colors
        while True:
            # blue
            led.set_all(0xff0000)
            sleep(1)
            # off
            led.set_all(0x000000)
            sleep(1)

    main()
