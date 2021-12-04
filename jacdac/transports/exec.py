import threading
from jacdac.bus import Transport
import subprocess

from jacdac.util import buf2hex, hex2buf

class ExecTransport(Transport):
    def __init__(self, exec: str):
        self.exec = exec
        self.open()

    def open(self) -> None:
        self.proc = subprocess.Popen(self.exec,
                                     shell=True, encoding="utf-8",
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE)
        t = threading.Thread(target=self.read_loop)
        t.start()

    def send(self, pkt: bytes) -> None:
        assert self.proc.stdin
        self.proc.stdin.write(buf2hex(pkt) + "\n")
        self.proc.stdin.flush()

    def read_loop(self):
        while True:
            assert self.proc.stdout
            ln = self.proc.stdout.readline()
            timestamp, hex = ln.split(" ")
            buf = None
            try:
                buf = hex2buf(hex.replace("\n", ""))
            except Exception as e:
                print(e)
            if buf and self.on_receive:
                self.on_receive(buf)
