# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class BrailleDisplayClient(Client):
    """
    A Braille pattern display module. This module display [unicode braille patterns](https://www.unicode.org/charts/PDF/U2800.pdf), country specific encoding have to be implemented by the clients.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_BRAILLE_DISPLAY, JD_BRAILLE_DISPLAY_PACK_FORMATS, role)
    

    @property
    def enabled(self) -> Optional[bool]:
        """
        Determins if the braille display is active., 
        """
        reg = self.register(JD_BRAILLE_DISPLAY_REG_ENABLED)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        reg = self.register(JD_BRAILLE_DISPLAY_REG_ENABLED)
        reg.set_values(value)


    @property
    def patterns(self) -> Optional[str]:
        """
        Braille patterns to show. Must be unicode characters between `0x2800` and `0x28ff`., 
        """
        reg = self.register(JD_BRAILLE_DISPLAY_REG_PATTERNS)
        values = reg.values()
        return cast(Optional[str], values[0] if values else None)

    @patterns.setter
    def patterns(self, value: str) -> None:
        self.enabled = True
        reg = self.register(JD_BRAILLE_DISPLAY_REG_PATTERNS)
        reg.set_values(value)


    @property
    def length(self) -> Optional[int]:
        """
        Gets the number of patterns that can be displayed., _: #
        """
        reg = self.register(JD_BRAILLE_DISPLAY_REG_LENGTH)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    
