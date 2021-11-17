from jacdac.devtools import createDevToolsBus
from .client import ButtonClient
from time import sleep

bus = createDevToolsBus()


def up():
    print("up")


def down():
    print("down")


def hold():
    print("hold")


btn1 = ButtonClient(bus, "btn1")
btn1.on_up(up)
btn1.on_down(down)
btn1.on_hold(hold)

while True:
    print(btn1.pressed)
    print(btn1.pressure)
    sleep(1000)
