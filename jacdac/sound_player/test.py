from jacdac.devtools import create_dev_tools_bus
from .server import SoundPlayServer, create_playsound

if __name__ == '__main__':
    def main():
        bus = create_dev_tools_bus()
        server = SoundPlayServer(
            bus, "./jacdac/sound_player/sounds", sound_player=create_playsound())
    main()
