class Transport:
    def receive(self, timeout_ms: int) -> bytes:
        raise NotImplementedError

    def send(self, pkt: bytes) -> None:
        pass


