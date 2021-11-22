from typing import cast
from jacdac.bus import Bus, Server, JDPacket
from .constants import *
from json import load, dump
from os import path, makedirs
from base64 import b64decode, b64encode


def value_to_json(value: bytearray) -> str:
    return b64encode(value).hex()


def json_to_value(text: str) -> bytearray:
    return bytearray(b64decode(bytearray.fromhex(text)))


class SettingsServer(Server):
    """
    Non-volatile key-value storage interface for storing settings.
    Implements a server for the `Settings <https://microsoft.github.io/jacdac-docs/services/settings>`_ service.
    """

    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_SETTINGS)
        if not path.exists(path.dirname(self.file_name)):
            makedirs(path.dirname(self.file_name))

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
        secret = key.startswith("$")
        value = bytearray(0)
        if not key is None and path.exists(self.file_name):
            with open(self.file_name, "rt") as f:
                settings = load(f)
                if key in settings:
                    if secret:  # don't return value
                        value = bytearray(0)
                    else:
                        value = json_to_value(settings[key])
        self.send_report(JDPacket.packed(
            JD_SETTINGS_CMD_GET, "z b", key, value))

    def _handle_delete(self, pkt: JDPacket):
        [key] = pkt.unpack("s")
        self.debug("delete key {}", key)
        with open(self.file_name, "wt") as f:
            settings = {}
            try:
                settings = load(f)
            except:
                pass
            if settings is None:
                settings = {}
            del settings[key]
            dump(settings, f)
        self.send_change_event()

    def _handle_set(self, pkt: JDPacket):
        [key, value] = pkt.unpack("z b")
        self.debug("set key {}", key)
        with open(self.file_name, "wt") as f:
            try:
                settings = load(f)
            except:
                settings = {}
            settings[key] = value_to_json(cast(bytearray, value))
            dump(settings, f)
        self.send_change_event()

    def _handle_clear(self, pkt: JDPacket):
        self.debug("clear keys")
        with open(self.file_name, "wt") as f:
            f.write("{}")
        self.send_change_event()

    def _handle_list(self, pkt: JDPacket):
        pass

    def _handle_list_keys(self, pkt: JDPacket):
        pass
