from .bus import Bus, Device, EV_DEVICE_CONNECT
from .transports.ws import WebSocketTransport


def on_device_connect(dev: Device):
    print("connected " + dev.short_id)


print("open http://localhost:8081 to diagnose python stack")
transport = WebSocketTransport("ws://localhost:8081")
bus = Bus(transport)
bus.on(EV_DEVICE_CONNECT, on_device_connect)
