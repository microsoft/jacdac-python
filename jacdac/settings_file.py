from io import TextIOWrapper
from typing import Any, List, Optional, Tuple
from .constants import *
from json import load, dump
from os import path, makedirs
from base64 import b64decode, b64encode


def value_to_json(value: bytearray) -> str:
    return b64encode(value).hex()


def json_to_value(text: str) -> bytearray:
    return bytearray(b64decode(bytearray.fromhex(text)))


class SettingsFile:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        if not path.exists(path.dirname(self.file_name)):
            makedirs(path.dirname(self.file_name))

    def is_secret(self, key: str) -> bool:
        return key.startswith("$")

    def _read_settings(self, f: TextIOWrapper) -> Any:
        try:
            return load(f)
        except:
            return {}

    def read(self, key: str, secrets: Optional[bool] = False) -> bytearray:
        if key is None or not path.exists(self.file_name):
            return bytearray(0)
        value = bytearray(0)
        with open(self.file_name, "r+") as f:
            settings = self._read_settings(f)
            if key in settings:
                secret = self.is_secret(key)
                if not secrets and secret:  # don't return value
                    value = bytearray(1)
                    value[0] = 0
                else:
                    value = json_to_value(settings[key])
        return value

    def delete(self, key: str) -> None:
        if key is None or not path.exists(self.file_name):
            return

        with open(self.file_name, "r+") as f:
            settings = self._read_settings(f)
            del settings[key]
            dump(settings, f)

    def write(self, key: str, value: bytearray) -> None:
        settings = {}
        if path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                settings = self._read_settings(f)
        with open(self.file_name, "w+") as f:
            settings[key] = value_to_json(value)
            dump(settings, f, skipkeys=True, sort_keys=True, indent=2)

    def clear(self):
        if not path.exists(self.file_name):
            return
        with open(self.file_name, "wt") as f:
            f.write("{}")

    def list(self, secrets: bool = False) -> List[Tuple[str, bytearray]]:
        if not path.exists(self.file_name):
            return []
        with open(self.file_name, "rt") as f:
            settings = self._read_settings(f)
            resp: List[Tuple[str, bytearray]] = []
            keys = settings.keys()
            for key in keys:
                value = bytearray(0)
                secret = self.is_secret(key)
                if not secrets and secret:  # don't return value
                    value = bytearray(1)
                    value[0] = 0
                else:
                    value = json_to_value(settings[key])
            return resp

    def list_keys(self) -> List[str]:
        if not path.exists(self.file_name):
            return []
        with open(self.file_name, "rt") as f:
            settings = self._read_settings(f)
            keys = settings.keys()
            return keys
