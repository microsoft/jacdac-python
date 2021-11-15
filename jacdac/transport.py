class Transport:
    # A base class for packet transports

    def receive(self, timeout_ms: int) -> bytes:
        # returns the next packet from the packet queue, None is empty
        raise NotImplementedError

    def send(self, pkt: bytes) -> None:
        # send a packet payload over the transport layer
        pass
