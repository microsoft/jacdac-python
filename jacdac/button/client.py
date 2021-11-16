from jacdac.bus import Bus, Client
from .constants import *


class ButtonClient(Client):
    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_BUTTON, role)
