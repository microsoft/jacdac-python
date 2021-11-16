from .bus import Bus
from .transports.ws import WebSocketTransport

print("open http://localhost:8081 to diagnose python stack")
transport = WebSocketTransport("ws://localhost:8081")
bus = Bus(transport)
