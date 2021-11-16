import threading
from typing import Any, Callable, TYPE_CHECKING, Coroutine, Union

if TYPE_CHECKING:
    from .bus import Bus

HandlerFn = Callable[..., Union[None, Coroutine[Any, Any, None]]]


class EventEmitter:
    def __init__(self, bus: 'Bus') -> None:
        self.bus = bus

    def emit(self, id: str, *args: object):
        self.bus.force_jd_thread()
        if not hasattr(self, "_listeners"):
            return
        idx = 0
        while idx < len(self._listeners):
            lid, fn, once = self._listeners[idx]
            if lid == id:
                def cb():
                    r = fn(*args)
                    if r is None:
                        return
                    self.bus.loop.create_task(r)
                self.bus.loop.call_soon(cb)
                if once:
                    del self._listeners[idx]
                    idx -= 1
            idx += 1

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

    # usage: await x.event("...")
    async def event(self, id: str):
        f = self.bus.loop.create_future()
        self.once(id, lambda: f.set_result(None))
        await f

    def wait_for(self, id: str):
        self.bus.force_non_jd_thread()
        cv = threading.Condition()
        happened = False

        def poke(*args: object):
            nonlocal happened
            with cv:
                happened = True
                cv.notify()

        self.once(id, poke)
        with cv:
            while not happened:
                cv.wait()
