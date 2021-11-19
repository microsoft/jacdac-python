# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class UvIndexClient(Client):
    """
    The UV Index is a measure of the intensity of ultraviolet (UV) rays from the Sun.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_UV_INDEX, JD_UV_INDEX_PACK_FORMATS, role)
    

    @property
    def uv_index(self) -> Optional[float]:
        """
        Ultraviolet index, typically refreshed every second., _: uv
        """
        reg = self.register(JD_UV_INDEX_REG_UV_INDEX)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def uv_index_error(self) -> Optional[float]:
        """
        (Optional) Error on the UV measure., _: uv
        """
        reg = self.register(JD_UV_INDEX_REG_UV_INDEX_ERROR)
        values = reg.values()
        return cast(Optional[float], values[0] if values else None)

    @property
    def variant(self) -> Optional[UvIndexVariant]:
        """
        (Optional) The type of physical sensor and capabilities., 
        """
        reg = self.register(JD_UV_INDEX_REG_VARIANT)
        values = reg.values()
        return cast(Optional[UvIndexVariant], values[0] if values else None)

    