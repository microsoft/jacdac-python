from typing import Callable, Optional
from jacdac.constants import JD_GET
from ..bus import Bus, Server, rand_u64
from ..packet import JDPacket
from .constants import JD_SERVICE_CLASS_RNG, JD_RNG_REG_RANDOM, JD_RNG_REG_VARIANT, RngVariant

RngGenerator = Callable[..., bytearray]


class RngServer(Server):
    """
    Generates random numbers using the python.getrandbits function.
    Implements a client for the `Random Number Generator <https://microsoft.github.io/jacdac-docs/services/rng>`_ service.
    """

    def __init__(self, bus: Bus, *, variant: Optional[RngVariant] = None, generator: RngGenerator = rand_u64) -> None:
        """Constructs a new rng server

        Args:
            bus (Bus): Jacdac bus
            variant (Optional[RngVariant], optional): Describes the random generation process. Defaults to None.
            generator (RngGenerator, optional): Function that generates 64 random bytes. Defaults to rand_u64.
        """
        super().__init__(bus, JD_SERVICE_CLASS_RNG)
        self.variant = variant
        self.generator = generator

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command
        if cmd == JD_GET(JD_RNG_REG_RANDOM):
            self._handle_get_random(pkt)
        elif cmd == JD_GET(JD_RNG_REG_VARIANT):
            self._handle_get_variant(pkt)
        else:
            super().handle_packet(pkt)

    def _handle_get_random(self, pkt: JDPacket):
        r = self.generator()
        self.debug("random {}", r.hex())
        self.send_report(JDPacket.packed(pkt.service_command, "b", r))

    def _handle_get_variant(self, pkt: JDPacket):
        if self.variant is None:
            self.send_report(pkt.not_implemented())
        else:
            self.send_report(JDPacket.packed(
                pkt.service_command, "u8", self.variant))
