from typing import Callable


class Transport:
    # A base class for packet transports

    on_receive: Callable[[bytes], None]

    def send(self, pkt: bytes) -> None:
        # send a packet payload over the transport layer
        pass
