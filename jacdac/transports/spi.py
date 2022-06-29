# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportMissingParameterType=false
from logging import getLogger
import threading
from typing import List
from time import sleep, monotonic
from jacdac.transport import Transport
from gpiod import Chip, Line, LineBulk, LINE_REQ_EV_RISING_EDGE, LINE_REQ_DIR_OUT # type: ignore
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

t0 = None
def millis():
    global t0
    if t0 is None:
        t0 = monotonic()
    return round( (monotonic() - t0) * 1000 )

class SpiTransport(Transport):
    def __init__(self):
        self.logger = getLogger(__name__)
        self.chip: Chip = None
        self.rxtx: LineBulk = None
        self.spi: SpiDev = None
        self.sendQueue: List[bytes] = []
        self._poke_cond = threading.Condition()

        try:
            self._open()
        finally:
            self._finalizer = finalize(self, self._cleanup, self.chip, self.spi)

    def _open(self) -> None:
        self.logger.debug("open")
        self.sendQueue: List[bytes] = []
        self.logger.debug("select chip")
        self.chip = Chip(RPI_CHIP)
        # monitor rx,tx in bulk
        self.logger.debug("request rx,tx")
        self.rxtx = self.chip.get_lines([RPI_PIN_RX_READY, RPI_PIN_TX_READY])
        self.rxtx.request(consumer = CONSUMER, type = LINE_REQ_EV_RISING_EDGE)
        self._flip_reset()
        self.logger.debug("open device")
        self.spi = SpiDev()
        self.spi.open(0, 0)        
        self.spi.max_speed_hz = 15600000
        self.spi.bits_per_word = 8
        self.logger.debug("start read loop")
        read_thread = threading.Thread(target=self._read_loop)
        read_thread.daemon = True
        read_thread.start()
        wait_thread = threading.Thread(target=self._io_wait_loop)
        wait_thread.daemon = True
        wait_thread.start()

    @classmethod
    def _cleanup(cls, chip: Chip, spi: SpiDev):
        if not chip is None:
            try:
                chip.close()
                #print("chip closed")
            except:
                print("error: chip failed to close")

        if not spi is None:
            try:
                spi.close()
                print("device closed")
            except:
                print("error: device failed to close")
    
    def close(self):
        self.logger.debug("close")
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
        self.logger.debug("reset bridge")
        self.sendQueue = []
        rst: Line = self.chip.get_line(RPI_PIN_RST)
        try:
            rst.request(consumer = CONSUMER, type = LINE_REQ_DIR_OUT)
            rst.set_value(0)
            sleep(0.01)
            rst.set_value(1)
        finally:
            rst.release()

    def send(self, pkt: bytes) -> None:
        # print("JD %d %s TX" % (millis(), buf2hex(pkt)))
        self.sendQueue.append(pkt)
        self._poke()

    def _read_loop(self) -> None:
        try:
            self._poke_cond.acquire()
            while True:
                self._poke_cond.wait()
                self._transfer()
        except:
            self.close()
            raise

    def _poke(self) -> None:
        self._poke_cond.acquire()
        self._poke_cond.notify()
        self._poke_cond.release()

    def _io_wait_loop(self) -> None:
        try:
            while True:
                ev_lines = self.rxtx.event_wait(nsec = 500 * 1000000) # List[Line]
                if ev_lines:
                    # need to read events, otherwise we get woken up again immedietly
                    for line in ev_lines:
                        line.event_read()
                    self._poke()
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

        if not sendtx and not rxReady:
            return False

        # debug("transfer rx:" + str(rx) + ", tx: " + str(tx) + ", queue: " + str(len(self.sendQueue)))

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

        rxqueue = bytearray(self.spi.xfer2(txqueue))

        if rxqueue is None:
            self.logger.debug("recv failed")
            return False
        
        framep = 0
        while framep + 4 < len(rxqueue):
            frame2 = rxqueue[framep + 2]
            if frame2 == 0:
                # print("empty frame")
                break
            sz = frame2 + 12
            if framep + sz > len(rxqueue):
                self.logger.debug("frame size out of range")
                break
            frame0 = rxqueue[framep]
            frame1 = rxqueue[framep + 1]
            frame3 = rxqueue[framep + 3]
            if frame0 == 0xff and frame1 == 0xff and frame3 == 0xff :
                # skip bogus packet
                pass
            else:
                buf = bytearray(rxqueue[framep:framep+sz])
                # print("JD %d %s RX" % (millis(), buf2hex(buf)))
                if buf and self.on_receive:
                    self.on_receive(buf)
            sz = (sz + 3) & ~3
            framep += sz
        # and we're done
        return True
