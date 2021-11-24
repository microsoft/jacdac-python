from jacdac import Bus
from jacdac.humidity import HumidityClient
from jacdac.thermometer import ThermometerClient
import csv
from time import sleep

if __name__ == '__main__':
    def main():
        bus = Bus()
        humidity_sensor = HumidityClient(bus, "weather.hum")
        thermometer = ThermometerClient(bus, "weather.temp")
        with open('weather.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=', ', )
            while True:
                h = humidity_sensor.humidity
                t = thermometer.temperature
                writer.writerow([h, t])
                sleep(1)
    main()
