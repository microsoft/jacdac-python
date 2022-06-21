from typing import Callable, Optional


class Transport:
    """A base class for packet transports"""

    on_receive: Optional[Callable[[bytes], None]] = None
    # Callback to report a received packet to the bus

    def send(self, pkt: bytes) -> None:
        # send a packet payload over the transport layer
        pass