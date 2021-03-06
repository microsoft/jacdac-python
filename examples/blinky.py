from jacdac.bus import Bus
from jacdac.led import LedClient
from time import sleep

if __name__ == '__main__':
    def main():
        from logging import basicConfig, INFO
        basicConfig(level=INFO)
        bus = Bus()
        led = LedClient(bus, "led")
        led.brightness = 0.5
        # fade between colors
        while True:
            # blue
            led.set_all((255, 0, 0))
            sleep(1)
            # off
            led.set_all((0, 0, 0))
            sleep(1)

    main()
