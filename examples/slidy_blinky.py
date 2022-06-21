from jacdac import Bus
from jacdac.led import LedClient
from jacdac.potentiometer import PotentiometerClient
from time import sleep

if __name__ == '__main__':
    def main():
        bus = Bus()
        led = LedClient(bus, "led")
        slider = PotentiometerClient(bus, "slider")
        led.set_all(0x0000ff)
        # fade between colors
        while True:
            position = slider.position or 0.
            brightness = position / 100.
            # change brightness
            led.brightness = brightness
            sleep(1)

    main()
