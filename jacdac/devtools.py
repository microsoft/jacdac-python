from .bus import Bus, Device, EV_DEVICE_CONNECT
from .transports.ws import WebSocketTransport


def createDevToolsBus():
    # Starts a Jacdac bus connected to the local detools websocket server
    # at ws://localhost:8081
    print("jacdac-python dev tools")
    print("run scripts/devtools.sh to launch the development server")
    print("open http://localhost:8081 to connect")
    transport = WebSocketTransport("ws://localhost:8081")
    bus = Bus(transport)
    return bus


if __name__ == "__main__":
    createDevToolsBus()
