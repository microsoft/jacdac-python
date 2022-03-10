from jacdac import Bus
from jacdac.led import LedClient
from jacdac import LoggerPriority
from time import sleep

if __name__ == '__main__':
    def main():
        bus = Bus()
        led = LedClient(bus, "led")
        speed = 0
        brightness = 128
        # fade between colors
        while True:
            # blue
            led.animate(0, 0, brightness, speed)
            sleep(1)
            # off
            led.animate(brightness, 0, 0, speed)
            sleep(1)

    main()
