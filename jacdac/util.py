import binascii
import time
from typing import List, Tuple, Union, cast

_hex = "0123456789abcdef"


def now():
    return int(time.monotonic() * 1000)

def hex_num(n: int, len: int = 8):
    r = "0x"
    for i in range(len):
        r += _hex[(n >> ((len - 1 - i) * 4)) & 0xf]
    return r


def buf2hex(buf: bytes):
    return binascii.hexlify(buf).decode()
    # r = ""
    # # is this quadartic?
    # for b in buf:
    #     r += _hex[b >> 4] + _hex[b & 0xf]
    # return r


def hex2buf(s: str):
    return binascii.unhexlify(s)
    # r = bytearray(len(s) >> 1)
    # for idx in range(0, len(s), 2):
    #     r[idx >> 1] = (_hex.index(s[idx].lower()) <<
    #                    4) | _hex.index(s[idx+1].lower())
    # return r


def u16(buf: bytes, off: int):
    return buf[off] | (buf[off+1] << 8)


def set_u16(buf: bytearray, off: int, val: int):
    buf[off] = val & 0xff
    buf[off + 1] = val >> 8


def u32(buf: bytes, off: int):
    return buf[off] | (buf[off+1] << 8) | (buf[off+2] << 16) | (buf[off+3] << 24)


def hash(buf: bytes, bits: int = 30):
    # return busio.JACDAC.__dict__["hash"](buf, bits)
    if bits < 1:
        return 0
    h = fnv1(buf)
    if bits >= 32:
        return h >> 0
    else:
        return ((h ^ (h >> bits)) & ((1 << bits) - 1))


def fnv1(data: bytes):
    h = 0x811c9dc5
    for i in range(len(data)):
        h = ((h * 0x1000193) & 0xffff_ffff) ^ data[i]
    return h


def short_id(longid: Union[bytes, str]):
    if isinstance(longid, str):
        longid = hex2buf(longid)
    h = hash(longid)
    return (
        chr(0x41 + h % 26) +
        chr(0x41 + (h // 26) % 26) +
        chr(0x30 + (h // (26 * 26)) % 10) +
        chr(0x30 + (h // (26 * 26 * 10)) % 10)
    )


def crc16(buf: bytes, start: int = 0, end: int = None):
    if end is None:
        end = len(buf)
    crc = 0xffff
    while start < end:
        data = buf[start]
        start += 1
        x = (crc >> 8) ^ data
        x ^= x >> 4
        crc = ((crc << 8) ^ (x << 12) ^ (x << 5) ^ x) & 0xffff
    return crc


def color_to_rgb(rgb: Union[int, Tuple[int, int, int], List[int]], default: Tuple[int, int, int]=(0, 0, 0)) -> Tuple[int, int, int]:
    """
    Maps various format to a r,g,b tuple
    """
    if rgb is None:
        return default
    elif type(rgb) == int:
        irgb = cast(int, rgb)
        r = (irgb >> 16) & 0xff
        g = (irgb >> 8) & 0xff
        b = (irgb >> 0) & 0xff
    elif type(rgb) == tuple:
        trgb = cast(Tuple[int, int, int], rgb)
        r = (trgb[0]) & 0xff
        g = (trgb[1]) & 0xff
        b = (trgb[2]) & 0xff
    else:
        lrgb = cast(List[int], rgb)
        r = (lrgb[0]) & 0xff
        g = (lrgb[1]) & 0xff
        b = (lrgb[2]) & 0xff
    return (r, g, b)
