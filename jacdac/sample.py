from .bus import *
from .button.client import ButtonClient
from .accelerometer.constants import *


def acc_sample(bus: Bus):
    acc = Client(bus, JD_SERVICE_CLASS_ACCELEROMETER,
                 JD_ACCELEROMETER_PACK_FORMATS,  "acc")

    async def acc_ev(pkt: JDPacket):
        print("acc 0x%x" % pkt.event_code)
        v = await acc.register(JD_ACCELEROMETER_REG_FORCES).query_async(refresh_ms=50)
        print(v.hex())
    acc.on(EV_EVENT, acc_ev)

    btn = ButtonClient(bus, "btn")

    async def btn_ev(pkt: JDPacket):
        print("btn", pkt.event_code, len(pkt.data) and pkt.unpack("u32"))
        v = await btn.register(13).query_async()
        print(v.hex())
    btn.on(EV_EVENT, btn_ev)
