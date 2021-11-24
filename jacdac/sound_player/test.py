from ..bus import Bus
from .server import SoundPlayServer, create_playsound

if __name__ == '__main__':
    def main():
        bus = Bus()
        server = SoundPlayServer(
            bus, "./jacdac/sound_player/sounds", sound_player=create_playsound())
    main()
