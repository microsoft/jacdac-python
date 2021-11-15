from typing import List
from websocket import WebSocketApp
from transport import Transport

# TODO import Transport
# use pylance 3.10 for union type notation
class WebSocketTransport(Transport):
    url: str
    ws: WebSocketApp
    pkts: List[bytes]

    def __init__(self, url: str):
        self.url = url
        self.open()
        self.pkts = []

    def open(self) -> None:
        ws = WebSocketApp(self.url,
                          on_open=self.on_open,
                          on_message=self.on_message,
                          on_error=self.on_error,
                          on_close=self.on_close)
        ws.run_forever()

    def receive(self, timeout_ms: int) -> bytes:
        # TODO: concurrency
        return self.pkts.pop(0)

    def send(self, pkt: bytes) -> None:
        self.ws.send(pkt)

    def on_message(self, ws: WebSocketApp, message: bytes):
        # TODO: concurrency
        self.pkts.append(message)

    def on_error(self, ws: WebSocketApp, error: str):
        print(error)

    def on_close(self, ws: WebSocketApp, close_status_code: int, close_msg: str):
        print("### closed ###")

    def on_open(self, ws: WebSocketApp):
        print("### open ###")
