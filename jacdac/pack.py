import struct
from typing import Any, List, Optional, Tuple, Union, cast

_fmts = {
    "u64": "<Q",
    "u32": "<I",
    "u16": "<H",
    "u8":  "<B",
    "i64": "<q",
    "i32": "<i",
    "i16": "<h",
    "i8":  "<b",
    "f32": "<f",
    "f64": "<d",
}


class _TokenParser:
    # c0: number
    # size: number
    # div: number
    # fp = 0
    # nfmt: NumberFormat
    # nfmt2: boolean
    # word: string
    # is_array: boolean

    def __init__(self, fmt: str):
        self.fmt = fmt
        self.fp: int = 0

    def parse(self):
        self.div: int = 1
        self.is_array: bool = False

        fmt = self.fmt
        while self.fp < len(fmt):
            endp = self.fp
            while endp < len(fmt) and not fmt[endp].isspace():
                endp += 1
            word = fmt[self.fp:endp]
            self.fp = endp + 1
            if word == "":
                continue

            dot_idx = word.index(".") if "." in word else -1
            c0 = word[0]
            # "u10.6" -> "u16", div = 1 << 6
            if (c0 == "i" or c0 == "u") and dot_idx >= 0:
                sz0 = int(word[1: dot_idx])
                sz1 = int(word[dot_idx + 1:])
                word = "%s%d" % (word[0], sz0 + sz1)
                self.div = 1 << sz1

            self.size = -1
            c1 = ""

            if word.endswith("[]"):
                word = word[0:-2]
                self.is_array = True

            if len(word) >= 2:
                c1 = word[1]
                if c1 == "[":
                    ep = word.index("]")
                    self.size = int(word[2:ep])

            self.word = word
            if word in _fmts:
                self.nfmt = _fmts[word]
                self.size = struct.calcsize(self.nfmt)
                self.c0: str = ""
            else:
                self.nfmt = None
                if c0 == "r":
                    if c1 != ":":
                        c0 = ""
                elif c0 == "s" or c0 == "b" or c0 == "x":
                    if len(word) != 1 and self.size == -1:
                        c0 = ""
                elif c0 == "z":
                    if len(word) != 1:
                        c0 = ""
                else:
                    c0 = ""
                if c0 == "":
                    raise ValueError("invalid format: %s" % word)
                self.c0 = c0

            return True
        return False


BasePackType = Union[int, float, str, bytes]
PackType = Union[BasePackType, List[BasePackType], Tuple[BasePackType]]
PackTuple = Tuple[PackType, ...]

def _jdunpack_core(buf: bytes, fmt: str, repeat: int) -> PackTuple:
    repeat_res: List[PackTuple] = []
    res: List[PackType] = []
    off: int = 0
    fp0 = 0
    parser = _TokenParser(fmt)
    if repeat and len(buf) == 0:
        return ()
    while parser.parse():
        if parser.is_array and not repeat:
            return tuple(res) + _jdunpack_core(buf[off:], fmt[fp0:], 1)

        fp0 = parser.fp
        sz = parser.size
        c0 = parser.c0
        if c0 == "z":
            endoff = off
            while (endoff < len(buf) and buf[endoff] != 0):
                endoff += 1
            sz = endoff - off
        elif sz < 0:
            sz = len(buf) - off

        if parser.nfmt is not None:
            v = struct.unpack_from(parser.nfmt, buf, off)[0]
            if (parser.div != 1):
                v /= parser.div
            res.append(v)
            off += parser.size
        else:
            subbuf = buf[off:off+sz]
            if c0 == "z" or c0 == "s":
                zerop = 0
                while (zerop < len(subbuf) and subbuf[zerop] != 0):
                    zerop += 1
                res.append(subbuf[0:zerop].decode("utf8"))
            elif c0 == "b":
                res.append(subbuf)
            elif c0 == "x":
                pass  # skip padding
            elif c0 == "r":
                return tuple(res) + _jdunpack_core(subbuf, fmt[fp0:], 2)
            else:
                assert False
            off += len(subbuf)
            if (c0 == "z"):
                off += 1

        if repeat and parser.fp >= len(fmt):
            parser.fp = 0
            if repeat == 2:
                repeat_res.append(tuple(res))
                res = []
            if (off >= len(buf)):
                break

    if repeat == 2:
        if len(res):
            repeat_res.append(tuple(res))
        return tuple(repeat_res)  # type: ignore
    else:
        return tuple(res)


def jdunpack(buf: bytes, fmt: str) -> PackTuple:
    if fmt in _fmts:
        t = struct.unpack(_fmts[fmt], buf)
        return (t[0],)
    return _jdunpack_core(buf, fmt, 0)


def _jdpack_core(trg: Optional[bytearray], fmt: str, data: List[PackType], off: int) -> int:
    idx = 0
    parser = _TokenParser(fmt)
    while parser.parse():
        c0 = parser.c0

        if c0 == "x":
            # skip padding
            off += parser.size
            continue

        if c0 == "r":
            fmt0 = fmt[parser.fp:]
            for velt in data[idx:]:
                off = _jdpack_core(trg, fmt0, cast(List[PackType], velt), off)
            idx = len(data)
            break

        if (parser.is_array):
            arr = data[idx:]
            idx = len(data)
        else:
            arr = [data[idx]]
            idx += 1

        for v in arr:
            if parser.nfmt is not None:
                if not isinstance(v, int) and not isinstance(v, float):
                    raise ValueError("expecting number, got %s" % v)
                if trg:
                    vp = int(v * parser.div)
                    struct.pack_into(parser.nfmt, trg, off, vp)
                off += parser.size
            else:
                if isinstance(v, str):
                    if (c0 == "z"):
                        buf = (v + "\u0000").encode("utf-8")
                    elif (c0 == "s"):
                        buf = v.encode("utf-8")
                    else:
                        raise ValueError("unexpected string")
                elif isinstance(v, bytes) or isinstance(v, bytearray):
                    # assume buffer
                    if (c0 == "b"):
                        buf = cast(bytes, v)
                    else:
                        raise ValueError("unexpected buffer")
                else:
                    raise ValueError("expecting string, bytes, bytearray")

                sz = parser.size
                if sz >= 0:
                    if len(buf) > sz:
                        buf = buf[0:sz]
                else:
                    sz = len(buf)

                if trg:
                    trg[off:off+len(buf)] = buf
                off += sz

    if len(data) > idx:
        raise ValueError("format too short")

    return off


def jdpack(fmt: str, *args: PackType) -> bytes:
    if fmt in _fmts:
        assert len(args) == 1
        return struct.pack(_fmts[fmt], args[0])

    data = cast(List[PackType], args)
    k = _jdpack_core(None, fmt, data, 0)
    res = bytearray(k)
    _jdpack_core(res, fmt, data, 0)
    return res


# TODO: move out to some test file?
def _jdpack_test():
    import json

    def default(o: Any):
        if isinstance(o, bytes) or isinstance(o, bytearray):
            return o.hex()
        raise TypeError("can't encode '%s'" % o)

    def stringify(o: Any):
        return json.dumps(o, default=default)

    def test_one(fmt: str, data0: List[Any], expected_payload: str = None):
        def checksame(a: Any, b: Any):
            def fail(msg: str):
                raise ValueError("jdpack test error: %s (at %s; a=%s; b=%s)" %
                                 (msg, fmt, stringify(a), stringify(b)))
            if a == b or stringify(a) == stringify(b):
                return
            fail("not the same")

        buf = jdpack(fmt, *data0)
        data1 = jdunpack(buf, fmt)
        buf_hex = buf.hex()
        print("%s->%s->%s->%s" %
              (stringify(data0), fmt, buf_hex, stringify(data1)))
        if (expected_payload is not None and expected_payload != buf_hex):
            raise ValueError("jdpack test error: payload %s, exected %s" % (
                buf_hex, expected_payload))
        checksame(data0, data1)

    test_one("i8", [-42])
    test_one("u16", [42])
    test_one("u16 u16 i16", [42, 77, -10])
    test_one("u16 z s", [42, "foo", "bar"])
    test_one("u32 z s", [42, "foo", "bar"])
    test_one("i8 z s", [42, "foo", "bar"])
    test_one("u8 z s", [42, "foo12", "bar"])
    test_one("u8 r: u8 z", [42, [17, "xy"], [18, "xx"]])
    test_one("z b", ["foo12", b'bar'])
    test_one("u16 r: u16", [42, [17], [18]])
    test_one("i8 s[9] u16 s[10] u8", [-100, "foo", 1000, "barbaz", 250])
    test_one("i8 x[4] s[9] u16 x[2] s[10] x[3] u8",
             [-100, "foo", 1000, "barbaz", 250])
    test_one("u16 u16[]", [42, 17, 18])
    test_one("u16 u16[]", [42, 18])
    test_one("u16 u16[]", [42])
    test_one("u16 z[]", [42, "foo", "bar", "bz"])
    test_one(
        "b[8] u32 u8 s",
        [b'\xa1\xb2\xc3\xd4\xe5\xf6\xa7\xb8', 0x12345678, 0x42, "barbaz"],
        expected_payload="a1b2c3d4e5f6a7b8785634124262617262617a"
    )


if __name__ == "__main__":
    _jdpack_test()
