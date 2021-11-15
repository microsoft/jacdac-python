from websocket import WebSocketApp
from ..transport import Transport


class WebSocketTransport(Transport):
    # A websocket-based transport
    #

    url: str
    ws: WebSocketApp

    def __init__(self, url: str):
        self.url = url
        self.open()

    def open(self) -> None:
        self.ws = WebSocketApp(self.url,
                          on_open=self.on_open,
                          on_message=self.on_message,
                          on_error=self.on_error,
                          on_close=self.on_close)
        self.ws.run_forever() # type: ignore

    def send(self, pkt: bytes) -> None:
        self.ws.send(pkt)  # type: ignore

    def on_message(self, ws: WebSocketApp, message: bytes):
        if self.on_receive:
            self.on_receive(message)

    def on_error(self, ws: WebSocketApp, error: str):
        print(error)

    def on_close(self, ws: WebSocketApp, close_status_code: int, close_msg: str):
        print("### closed ###")

    def on_open(self, ws: WebSocketApp):
        print("### open ###")
