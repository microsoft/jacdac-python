# pyright: reportGeneralTypeIssues=false
import threading
from typing import Optional
import websocket # type: ignore
from jacdac.transport import Transport


class WebSocketTransport(Transport):
    def __init__(self, url: str):
        self.url = url
        self.ws: Optional[websocket.WebSocketApp] = None
        self.opened = False
        self.open()

    def open(self) -> None:
        self.ws = websocket.WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        t = threading.Thread(target=self.ws.run_forever)  # type: ignore
        t.daemon = True
        t.start()

    def send(self, pkt: bytes) -> None:
        if self.opened:
            self.ws.send(pkt, opcode=2)  # type: ignore

    def on_message(self, _, message: bytes):
        if self.on_receive:
            self.on_receive(message)

    def on_error(self, _, error: str):
        if self.opened:
            print(error)

    def on_close(self, _, close_status_code: int, close_msg: str):
        self.opened = False

    def on_open(self, _):
        print("devtools server connected at " + self.url)
        self.opened = True
