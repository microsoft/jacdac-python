import threading
from time import sleep
from jacdac.bus import Transport
from jacdac.util import buf2hex, hex2buf
from gpiod import Chip, Line, LineBulk, LINE_REQ_EV_RISING_EDGE, LINE_REQ_FLAG_ACTIVE_LOW, LINE_REQ_DIR_OUT, LINE_REQ_DIR_IN

# https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/gpiodmodule.c?h=v1.6.x&id=27cacfe377114f6acf67cd943d1ca01bb30e0f2b
RPI_CHIP = 'pinctrl-bcm2835'
RPI_PIN_TX_READY = 24
RPI_PIN_RX_READY = 25
RPI_PIN_RST = 22
CONSUMER = "jacdac"

class SpiTransport(Transport):
    def __init__(self):
        self.chip: Chip = None
        self.rxtx: LineBulk = None
        self.rst: Line = None
        self.open()

    def open(self) -> None:
        print("spi: select chip")
        self.chip = Chip(RPI_CHIP)
        # monitor rx,tx in bulk
        print("spi: request rx,tx")
        self.rxtx = self.chip.get_lines([RPI_PIN_RX_READY, RPI_PIN_TX_READY])
        self.rxtx.request(consumer = CONSUMER, type = LINE_REQ_EV_RISING_EDGE, flags = LINE_REQ_FLAG_ACTIVE_LOW)

        self._flip_reset()

        t = threading.Thread(target=self.read_loop)
        t.start()

    def __exit__(self, type, value, traceback):
        if not self.rxtx is None:
            self.rxtx.release()
            self.rxtx = None
        if not self.chip is None:
            self.chip.close()
            self.chip = None
        

    def _flip_reset(self) -> None:
        print("spi: flip reset")
        rst = self.chip.get_line(RPI_PIN_RST)
        try:
            rst.request(consumer = CONSUMER, type = LINE_REQ_DIR_OUT, flags = LINE_REQ_FLAG_ACTIVE_LOW)
            rst.set_value(0)
            sleep(0.001)
            rst.set_value(1)
            rst.set_direction_input()
        finally:
            rst.release()

    def send(self, pkt: bytes) -> None:
        print("send")

    def read_loop(self) -> None:
        while True:
            ev_lines = self.rxtx.event_wait(nsec = 1) # List[Line]
            if ev_lines:
                print("read")
