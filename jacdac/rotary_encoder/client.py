from jacdac.bus import Bus, Client
from .constants import *
from typing import Union, cast


class RotaryEncoderClient(Client):
    """
    An incremental rotary encoder - converts angular motion of a shaft to digital signal.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_ROTARY_ENCODER,
                         JD_ROTARY_ENCODER_PACK_FORMATS, role)

    @property
    def position(self) -> Union[int, None]:
        """
        Upon device reset starts at `0` (regardless of the shaft position).
        Increases by `1` for a clockwise "click", by `-1` for counter-clockwise., #
        """
        reg = self.register(JD_ROTARY_ENCODER_REG_POSITION)
        value = reg.value(0)
        return cast(Union[int, None], value)

    @property
    def clicks_per_turn(self) -> Union[int, None]:
        """
        (Optional) This specifies by how much `position` changes when the crank does 360 degree turn. Typically 12 or 24., #
        """
        reg = self.register(JD_ROTARY_ENCODER_REG_CLICKS_PER_TURN)
        value = reg.value(0)
        return cast(Union[int, None], value)
