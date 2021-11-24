import threading
from typing import Optional
from websocket import WebSocketApp
from jacdac.bus import Transport


class WebSocketTransport(Transport):
    def __init__(self, url: str):
        self.url = url
        self.ws: Optional[WebSocketApp] = None
        self.opened = False
        self.open()

    def open(self) -> None:
        self.ws = WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        t = threading.Thread(target=self.ws.run_forever)  # type: ignore
        t.start()

    def send(self, pkt: bytes) -> None:
        if self.opened:
            self.ws.send(pkt, opcode=2)  # type: ignore

    def on_message(self, ws: WebSocketApp, message: bytes):
        if self.on_receive:
            self.on_receive(message)

    def on_error(self, ws: WebSocketApp, error: str):
        if self.opened:
            print(error)

    def on_close(self, ws: WebSocketApp, close_status_code: int, close_msg: str):
        self.opened = False

    def on_open(self, ws: WebSocketApp):
        print("devtools server connected")
        self.opened = True
