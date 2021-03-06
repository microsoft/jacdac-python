# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional


class MidiOutputClient(Client):
    """
    A MIDI output device.
    Implements a client for the `MIDI output <https://microsoft.github.io/jacdac-docs/services/midioutput>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_MIDI_OUTPUT, JD_MIDI_OUTPUT_PACK_FORMATS, role)


    @property
    def enabled(self) -> Optional[bool]:
        """
        Opens or closes the port to the MIDI device, 
        """
        return self.register(JD_MIDI_OUTPUT_REG_ENABLED).bool_value()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.register(JD_MIDI_OUTPUT_REG_ENABLED).set_values(value)



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
    
