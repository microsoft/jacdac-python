# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast


class MidiOutputClient(Client):
    """
    A MIDI output device.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_MIDI_OUTPUT, JD_MIDI_OUTPUT_PACK_FORMATS, role)
    

    @property
    def enabled(self) -> Optional[bool]:
        """
        Opens or closes the port to the MIDI device, 
        """
        reg = self.register(JD_MIDI_OUTPUT_REG_ENABLED)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        reg = self.register(JD_MIDI_OUTPUT_REG_ENABLED)
        reg.set_values(value) # type: ignore



    def clear(self, ) -> None:
        """
        Clears any pending send data that has not yet been sent from the MIDIOutput's queue.
        """
        self.send_cmd_packed(JD_MIDI_OUTPUT_CMD_CLEAR, )

    def send(self, data: bytes) -> None:
        """
        Enqueues the message to be sent to the corresponding MIDI port
        """
        self.send_cmd_packed(JD_MIDI_OUTPUT_CMD_SEND, data)
    
