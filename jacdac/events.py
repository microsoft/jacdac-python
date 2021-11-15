from typing import Callable, TYPE_CHECKING
from .util import now, log

if TYPE_CHECKING:
    from .bus import Bus

HandlerFn = Callable[..., None]


class EventEmitter:
    def __init__(self, bus: 'Bus') -> None:
        self.bus = bus

    def emit(self, id: str, *args: object):
        if not hasattr(self, "_listeners"):
            return
        fns: list[HandlerFn] = []
        idx = 0
        while idx < len(self._listeners):
            lid, fn, once = self._listeners[idx]
            if lid == id:
                fns.append(fn)
                if once:
                    del self._listeners[idx]
                    idx -= 1
            idx += 1
        for fn in fns:
            t0 = now()
            fn(*args)
            d = now() - t0
            if d > 100:
                log("long running handler for '{}'; {}ms", id, d)

    def _init_emitter(self):
        if not hasattr(self, "_listeners"):
            self._listeners: list[tuple[str, HandlerFn, bool]] = []

    def on(self, id: str, fn: HandlerFn):
        self._init_emitter()
        self._listeners.append((id, fn, False))

    def once(self, id: str, fn: HandlerFn):
        self._init_emitter()
        self._listeners.append((id, fn, True))

    def off(self, id: str, fn: HandlerFn):
        self._init_emitter()
        for i in range(len(self._listeners)):
            id2, fn2, _ign = self._listeners[i]
            if id == id2 and fn is fn2:
                del self._listeners[i]
                return
        raise ValueError("no matching on() for off()")
