from jacdac.bus import Bus
from jacdac.humidity import HumidityClient
from jacdac.temperature import TemperatureClient
import csv
from time import sleep

if __name__ == '__main__':
    def main():
        bus = Bus()
        humidity_sensor = HumidityClient(bus, "weather.hum")
        temperature = TemperatureClient(bus, "weather.temp")
        with open('weather.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', )
            while True:
                h = humidity_sensor.humidity
                t = temperature.temperature
                writer.writerow([h, t])
                sleep(1)
    main()
