import threading
from typing import List, Optional
from time import sleep
from tokenize import Number
from jacdac.bus import Transport
from jacdac.util import buf2hex, hex2buf, now
from gpiod import Chip, Line, LineBulk, LINE_REQ_EV_RISING_EDGE, LINE_REQ_FLAG_ACTIVE_LOW, LINE_REQ_DIR_OUT # type: ignore
from spidev import SpiDev # type: ignore
from weakref import finalize

XFER_SIZE = 256
# https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/gpiodmodule.c?h=v1.6.x&id=27cacfe377114f6acf67cd943d1ca01bb30e0f2b
RPI_CHIP = 'pinctrl-bcm2835'
RPI_PIN_TX_READY = 24
RPI_PIN_RX_READY = 25
RPI_PIN_RST = 22
CONSUMER = "jacdac"
MAX_SEND_QUEUE_LEN = 10

class SpiTransport(Transport):
    def __init__(self):
        self.chip: Chip = None
        self.rxtx: LineBulk = None
        self.spi: SpiDev = None
        self.sendQueue: List[bytes] = []

        try:
            self._open()
        finally:
            self._finalizer = finalize(self, self._cleanup, self.chip, self.spi)

    def _open(self) -> None:
        self.sendQueue: List[bytes] = []
        print("spi: select chip")
        self.chip = Chip(RPI_CHIP)
        # monitor rx,tx in bulk
        print("spi: request rx,tx")
        self.rxtx = self.chip.get_lines([RPI_PIN_RX_READY, RPI_PIN_TX_READY])
        self.rxtx.request(consumer = CONSUMER, type = LINE_REQ_EV_RISING_EDGE, flags = LINE_REQ_FLAG_ACTIVE_LOW)
        self._flip_reset()
        print("spi: open device")
        self.spi = SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 15600000
        self.spi.bits_per_word = 8
        print("spi: start read loop")
        t = threading.Thread(target=self._read_loop)
        t.start()

    @classmethod
    def _cleanup(cls, chip: Chip, spi: SpiDev):
        if not chip is None:
            try:
                chip.close()
                print("spi: chip closed")
            except:
                print("error: chip failed to close")

        if not spi is None:
            try:
                spi.close()
                print("spi: device closed")
            except:
                print("error: device failed to close")
    
    def close(self):
        print("spi: close")
        chip = self.chip
        spi = self.spi
        if not chip is None or not spi is None:
            self.chip = None
            self.spi = None
            self.rxtx = None
            self.sendQueue = []
            self._cleanup(chip, spi)
            self._finalizer.detach()
        
    def _flip_reset(self) -> None:
        print("spi: reset bridge")
        self.sendQueue = []
        rst = self.chip.get_line(RPI_PIN_RST)
        try:
            rst.request(consumer = CONSUMER, type = LINE_REQ_DIR_OUT)
            rst.set_value(0)
            sleep(0.01)
            rst.set_value(1)
        finally:
            rst.release()

    def send(self, pkt: bytes) -> None:
        self.sendQueue.append(pkt)
        self._transfer()

    def _read_loop(self) -> None:
        try:
            while True:
                ev_lines = self.rxtx.event_wait(nsec = 1) # List[Line]
                if ev_lines:
                    self._transfer()
        except:
            self.close()
            raise

    def _read_ready_pins(self) -> List[int]:
        rxtxv = self.rxtx.get_values() 
        if rxtxv is None:
            return [0, 0]
        else:
            return rxtxv

    def _transfer(self) -> None:
        if len(self.sendQueue) > MAX_SEND_QUEUE_LEN:
            self._flip_reset()

        try:
            while self._transfer_frame():
                pass
        except:
            self.close()
            raise

    def _transfer_frame(self) -> bool:
        [rx, tx] = self._read_ready_pins()
        rxReady = rx != 0
        txReady = tx != 0
        sendtx = txReady and len(self.sendQueue) > 0

      #  print("spi: transfer rx:" + str(rx) + ", tx: " + str(tx) + ", queue: " + str(len(self.sendQueue)))

        if not sendtx and not rxReady:
            return False

        # allocate transfer buffers
        txqueue = bytearray(XFER_SIZE)

        # assemble packets into send buffer
        txq_ptr = 0
        while txReady and len(self.sendQueue) > 0:
            pkt = self.sendQueue[0]
            npkt = len(pkt)
            if txq_ptr + npkt > len(txqueue):
                break
            self.sendQueue.pop(0)
            txqueue[txq_ptr:txq_ptr+npkt] = pkt
            txq_ptr += (npkt + 3) & ~3

        if txq_ptr == 0 and not rxReady:
            return False

        rxqueue = bytearray(0)
        if txq_ptr > 0:
            txqueue = bytearray(txqueue[0::txq_ptr])
            print(str(now()) + " " + buf2hex(txqueue) + " send frame")
            rxqueue = bytearray(self.spi.xfer2(txqueue))
        elif rxReady:
            rxqueue = bytearray(self.spi.readbytes(XFER_SIZE))
        if rxReady:
            if rxqueue is None:
                print("recv failed")
                return False
            #print(str(now()) + " " + buf2hex(rxqueue) + " recv frame")
            
            framep = 0
            while framep + 4 < len(rxqueue) :
                frame2 = rxqueue[framep + 2]
                if frame2 == 0:
                    # print("spi: empty frame")
                    break
                sz = frame2 + 12
                if framep + sz > len(rxqueue):
                    print("spi: frame size out of range")
                    break
                frame0 = rxqueue[framep]
                frame1 = rxqueue[framep + 1]
                frame3 = rxqueue[framep + 3]
                if frame0 == 0xff and frame1 == 0xff and frame3 == 0xff :
                    # skip bogus packet
                    print("spi: skip bogus pkt")
                    pass
                else:
                    buf = bytearray(rxqueue[framep:framep+sz])
                    print("spi: recv pkt " + buf2hex(buf))
                    if buf and self.on_receive:
                        self.on_receive(buf)
                sz = (sz + 3) & ~3
                framep += sz
        # and we're done
        return True
