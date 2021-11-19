import sys
import threading
import queue
import random
import struct
from typing import List

from jacdac.bus import Transport

HF2_CMD_INFO = 0x0002
HF2_CMD_DMESG = 0x0010

HF2_FLAG_SERIAL_OUT = 0x80
HF2_FLAG_SERIAL_ERR = 0xc0
HF2_FLAG_CMDPKT_LAST = 0x40
HF2_FLAG_CMDPKT_BODY = 0x00
HF2_FLAG_MASK = 0xc0
HF2_SIZE_MASK = 63

HF2_STATUS_OK = 0x00
HF2_STATUS_INVALID_CMD = 0x01
HF2_STATUS_EXEC_ERR = 0x02
HF2_STATUS_EVENT = 0x80

# the eventId is overlayed on the tag+status; the mask corresponds
# to the HF2_STATUS_EVENT above
HF2_EV_MASK = 0x800000

HF2_CMD_JDS_CONFIG = 0x0020
HF2_CMD_JDS_SEND = 0x0021
HF2_EV_JDS_PACKET = 0x800020


class HF2Error(Exception):
    pass


class HF2Transport(Transport):
    def _write(self, buf: bytes):
        frame = bytearray(64)
        pos = 0
        while True:
            l = len(buf) - pos
            if l <= 0:
                break
            if l > 63:
                l = 63
                frame[0] = HF2_FLAG_CMDPKT_BODY
            else:
                frame[0] = HF2_FLAG_CMDPKT_LAST
            frame[0] |= l
            frame[1:1+l] = buf[pos:pos+l]
            self.serial.write(frame)  # type: ignore
            pos += l

    def _on_serial(self, buf: bytes, is_error: bool):
        self.log("serial: %s" % buf.decode("utf-8"))

    def _on_jd_pkt(self, buf: bytes):
        # self.log("jd: " + buf.hex())
        if self.on_receive:
            self.on_receive(buf)

    def _on_event(self, buf: bytes):
        (evid,) = struct.unpack("<I", buf[0:4])
        if evid == HF2_EV_JDS_PACKET:
            self._on_jd_pkt(buf[4:])
        else:
            self.log("unknown event: 0x%x" % evid)

    def _read_loop(self):
        frames: List[bytes] = []
        while True:
            buf: bytes = self.serial.read(64)  # type: ignore
            tp = buf[0] & HF2_FLAG_MASK
            l = buf[0] & 63
            frame = buf[1:1+l]
            if tp & HF2_FLAG_SERIAL_OUT:
                self._on_serial(frame, tp == HF2_FLAG_SERIAL_ERR)
                continue
            frames.append(frame)
            if tp == HF2_FLAG_CMDPKT_BODY:
                pass
            else:
                assert tp == HF2_FLAG_CMDPKT_LAST
                r = b''.join(frames)
                frames = []
                if r[2] & HF2_STATUS_EVENT:
                    self._on_event(r)
                else:
                    self._msgs.put(r)

    def log(self, msg: str):
        print("HF2: %s" % msg)

    def _error(self, msg: str):
        self.log("Error: %s" % msg)
        raise HF2Error("HF2: %s" % msg)

    def _talk(self, cmd: int, data: bytes = b'') -> bytes:
        with self._talk_lock:
            self._cmd_seq = (self._cmd_seq + 1) & 0xffff
            seq = self._cmd_seq
            payload = struct.pack("<IHH", cmd, seq, 0) + data
            self._write(payload)
            for repeat in range(3):
                try:
                    resp = self._msgs.get(block=True, timeout=1)
                except queue.Empty:
                    self._error("timeout for 0x%d" % cmd)
                (seq2, status, info) = struct.unpack("<HBB", resp[0:4])
                if seq != seq2:
                    self.log("packet out of sync (exp: %d, got: %d)" %
                             (seq, seq2))
                elif status == 0:
                    return resp[4:]
                else:
                    self._error("bad status: %d (info=%d) for 0x%x" %
                                (status, info, cmd))
            self._error("desync for 0x%x" % cmd)

    def _connect(self):
        info = self._talk(HF2_CMD_INFO)
        self.log("connected to '%s'" % info.decode("utf8"))
        self._talk(HF2_CMD_JDS_CONFIG, struct.pack("<I", 1))

    def send(self, pkt: bytes):
        self._talk(HF2_CMD_JDS_SEND, pkt)

    def __init__(self, portname: str) -> None:
        import serial
        self.serial: serial.Serial = serial.Serial(portname, 4_000_000)
        self._msgs: queue.Queue[bytes] = queue.Queue()
        self._cmd_seq = random.randint(0x1000, 0xffff)
        self._talk_lock = threading.Lock()
        self._reader_thread = threading.Thread(target=self._read_loop)
        self._reader_thread.start()
        self._connect()


if __name__ == "__main__":
    hf2 = HF2Transport(sys.argv[1])
