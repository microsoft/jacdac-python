from typing import cast
from jacdac.bus import Bus, Server, JDPacket, OutPipe
from jacdac.pack import jdpack
from .constants import *
from ..settings_file import SettingsFile


class SettingsServer(Server):
    """
    Non-volatile key-value storage interface for storing settings.
    Implements a server for the `Settings <https://microsoft.github.io/jacdac-docs/services/settings>`_ service.
    """

    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SETTINGS)
        self.settings = SettingsFile(self.file_name)

    @property
    def file_name(self) -> str:
        f = self.bus.settings_file_name
        if f is None:
            raise RuntimeError("settings file name not set")
        return f

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command
        if cmd == JD_SETTINGS_CMD_CLEAR:
            self._handle_clear(pkt)
        elif cmd == JD_SETTINGS_CMD_LIST_KEYS:
            self._handle_list_keys(pkt)
        elif cmd == JD_SETTINGS_CMD_LIST:
            self._handle_list(pkt)
        elif cmd == JD_SETTINGS_CMD_GET:
            self._handle_get(pkt)
        elif cmd == JD_SETTINGS_CMD_SET:
            self._handle_set(pkt)
        elif cmd == JD_SETTINGS_CMD_DELETE:
            self._handle_delete(pkt)
        return super().handle_packet(pkt)

    def _handle_get(self, pkt: JDPacket):
        key: str = cast(str, pkt.unpack("s")[0])
        value = self.settings.read(key)
        self.send_report(JDPacket.packed(
            JD_SETTINGS_CMD_GET, "z b", key, value))

    def _handle_delete(self, pkt: JDPacket):
        [key] = pkt.unpack("s")
        self.debug("delete key {}", key)
        self.settings.delete(cast(str, key))
        self.send_change_event()

    def _handle_set(self, pkt: JDPacket):
        [key, value] = pkt.unpack("z b")
        self.debug("set key {}", key)
        self.settings.write(cast(str, key), cast(bytearray, value))
        self.send_change_event()

    def _handle_clear(self, pkt: JDPacket):
        self.debug("clear keys")
        self.settings.clear()
        self.send_change_event()

    def _handle_list(self, pkt: JDPacket):
        pipe = OutPipe(self.bus, pkt)
        keys = self.settings.list()
        for key in keys:
            value = self.settings.read(key)
            pipe.write(bytearray(jdpack("z b", key, value)))
        pipe.close()

    def _handle_list_keys(self, pkt: JDPacket):
        pipe = OutPipe(self.bus, pkt)
        keys = self.settings.list()
        for key in keys:
            pipe.write(bytearray(jdpack("s", key)))
        pipe.close()
