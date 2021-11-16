from jacdac.bus import Bus, Server
from .constants import *


class UniqueBrainServer(Server):
    # A unique brain server

    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_UNIQUE_BRAIN)
