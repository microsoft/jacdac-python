from jacdac import Bus
from jacdac.led import LedClient
from time import sleep

if __name__ == '__main__':
    def main():
        bus = Bus()
        led = LedClient(bus, "led")
        led.brightness = 0.5
        # change between colors
        while True:
            # blue
            led.set_all(0x0000ff)
            sleep(1)
            # red
            led.set_all(0xff0000)
            sleep(1)
            # green
            led.set_all(0x00ff00)
            sleep(1)

    main()
