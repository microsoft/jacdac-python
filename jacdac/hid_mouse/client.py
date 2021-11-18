# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *



class HidMouseClient(Client):
    """
    Controls a HID mouse.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_HID_MOUSE, JD_HID_MOUSE_PACK_FORMATS, role)
    


    def set_button(self, buttons: HidMouseButton, event: HidMouseButtonEvent) -> None:
        """
        Sets the up/down state of one or more buttons.
        A ``Click`` is the same as ``Down`` followed by ``Up`` after 100ms.
        A ``DoubleClick`` is two clicks with ``150ms`` gap between them (that is, ``100ms`` first click, ``150ms`` gap, ``100ms`` second click).
        """
        self.send_cmd_packed(JD_HID_MOUSE_CMD_SET_BUTTON, buttons, event)

    def move(self, dx: int, dy: int, time: int) -> None:
        """
        Moves the mouse by the distance specified.
        If the time is positive, it specifies how long to make the move.
        """
        self.send_cmd_packed(JD_HID_MOUSE_CMD_MOVE, dx, dy, time)

    def wheel(self, dy: int, time: int) -> None:
        """
        Turns the wheel up or down. Positive if scrolling up.
        If the time is positive, it specifies how long to make the move.
        """
        self.send_cmd_packed(JD_HID_MOUSE_CMD_WHEEL, dy, time)
    
