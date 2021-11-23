from typing import Callable, cast

from jacdac.pack import jdpack
from ..bus import Bus, OutPipe, Server
from .constants import *
from ..packet import JDPacket
from os import path, listdir


def create_playsound() -> Callable[[str], None]:
    from playsound import playsound

    def play(f: str):
        playsound(f, False)
    return play


def create_pygame_mixer() -> Callable[[str], None]:
    from pygame import mixer
    mixer.init()

    def play(f: str):
        snd = mixer.Sound(f)
        snd.play()
    return play


class SoundPlayServer(Server):
    """A sound player server implementation.

    This server uses pygame.

    pip install pygame

    """

    def __init__(self, bus: Bus, sound_dir: str, *, instance_name: str = None, sound_player: Callable[[str], None] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SOUND_PLAYER, instance_name=instance_name)
        self.sound_dir = sound_dir
        self.sound_player = sound_player
        self.volume = 0.2

    def handle_packet(self, pkt: JDPacket):
        self.volume = self.handle_reg(
            pkt, JD_SOUND_PLAYER_REG_VOLUME, JD_SOUND_PLAYER_PACK_FORMATS[JD_SOUND_PLAYER_REG_VOLUME], self.volume)

        cmd = pkt.service_command
        if cmd == JD_SOUND_PLAYER_CMD_PLAY:
            self.handle_play(pkt)
        elif cmd == JD_SOUND_PLAYER_CMD_LIST_SOUNDS:
            self.handle_list_sounds(pkt)
        else:
            super().handle_packet(pkt)

    def handle_play(self, pkt: JDPacket):
        name = cast(str, pkt.unpack(
            JD_SOUND_PLAYER_PACK_FORMATS[JD_SOUND_PLAYER_CMD_PLAY])[0])
        for f in listdir(self.sound_dir):
            if path.basename(f) == name:
                fp = path.join(self.sound_dir, f)
                if self.sound_player:
                    self.sound_player(fp)
                break

    def handle_list_sounds(self, pkt: JDPacket):
        pipe = OutPipe(self.bus, pkt)
        files = listdir(self.sound_dir)
        for f in files:
            if f.endswith(".mp3") or f.endswith(".wav"):
                pipe.write(bytearray(jdpack("u32 s", 0, path.basename(f))))
        pipe.close()
