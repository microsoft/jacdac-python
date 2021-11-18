# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class ProtoTestClient(Client):
    """
    This is test service to validate the protocol packet transmissions between the browser and a MCU.
     * Use this page if you are porting Jacdac to a new platform.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_PROTO_TEST, JD_PROTO_TEST_PACK_FORMATS, role)
    

    @property
    def rw_bool(self) -> Optional[bool]:
        """
        A read write bool register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_BOOL)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @rw_bool.setter
    def rw_bool(self, value: bool) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_BOOL)
        reg.set_values(value)


    @property
    def ro_bool(self) -> Optional[bool]:
        """
        A read only bool register. Mirrors rw_bool., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_BOOL)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @property
    def rw_u32(self) -> Optional[int]:
        """
        A read write u32 register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_U32)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @rw_u32.setter
    def rw_u32(self, value: int) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_U32)
        reg.set_values(value)


    @property
    def ro_u32(self) -> Optional[int]:
        """
        A read only u32 register.. Mirrors rw_u32., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_U32)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @property
    def rw_i32(self) -> Optional[int]:
        """
        A read write i32 register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_I32)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @rw_i32.setter
    def rw_i32(self, value: int) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_I32)
        reg.set_values(value)


    @property
    def ro_i32(self) -> Optional[int]:
        """
        A read only i32 register.. Mirrors rw_i32., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_I32)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    @property
    def rw_string(self) -> Optional[str]:
        """
        A read write string register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_STRING)
        values = reg.values()
        return cast(Optional[str], values[0] if values else None)

    @rw_string.setter
    def rw_string(self, value: str) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_STRING)
        reg.set_values(value)


    @property
    def ro_string(self) -> Optional[str]:
        """
        A read only string register. Mirrors rw_string., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_STRING)
        values = reg.values()
        return cast(Optional[str], values[0] if values else None)

    @property
    def rw_bytes(self) -> Optional[bytes]:
        """
        A read write string register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_BYTES)
        values = reg.values()
        return cast(Optional[bytes], values[0] if values else None)

    @rw_bytes.setter
    def rw_bytes(self, value: bytes) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_BYTES)
        reg.set_values(value)


    @property
    def ro_bytes(self) -> Optional[bytes]:
        """
        A read only string register. Mirrors ro_bytes., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_BYTES)
        values = reg.values()
        return cast(Optional[bytes], values[0] if values else None)

    @property
    def rw_i8_u8_u16_i32(self) -> Optional[tuple[int, int, int, int]]:
        """
        A read write i8, u8, u16, i32 register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_I8_U8_U16_I32)
        values = reg.values()
        return cast(Optional[tuple[int, int, int, int]], values)

    @rw_i8_u8_u16_i32.setter
    def rw_i8_u8_u16_i32(self, value: tuple[int, int, int, int]) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_I8_U8_U16_I32)
        reg.set_values(*value)


    @property
    def ro_i8_u8_u16_i32(self) -> Optional[tuple[int, int, int, int]]:
        """
        A read only i8, u8, u16, i32 register.. Mirrors rw_i8_u8_u16_i32., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_I8_U8_U16_I32)
        values = reg.values()
        return cast(Optional[tuple[int, int, int, int]], values)

    @property
    def rw_u8_string(self) -> Optional[tuple[int, str]]:
        """
        A read write u8, string register., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RW_U8_STRING)
        values = reg.values()
        return cast(Optional[tuple[int, str]], values)

    @rw_u8_string.setter
    def rw_u8_string(self, value: tuple[int, str]) -> None:
        reg = self.register(JD_PROTO_TEST_REG_RW_U8_STRING)
        reg.set_values(*value)


    @property
    def ro_u8_string(self) -> Optional[tuple[int, str]]:
        """
        A read only u8, string register.. Mirrors rw_u8_string., 
        """
        reg = self.register(JD_PROTO_TEST_REG_RO_U8_STRING)
        values = reg.values()
        return cast(Optional[tuple[int, str]], values)

    def on_e_bool(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_bool is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_BOOL, handler)

    def on_e_u32(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_u32 is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_U32, handler)

    def on_e_i32(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_i32 is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_I32, handler)

    def on_e_string(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_string is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_STRING, handler)

    def on_e_bytes(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_bytes is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_BYTES, handler)

    def on_e_i8_u8_u16_i32(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_i8_u8_u16_i32 is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_I8_U8_U16_I32, handler)

    def on_e_u8_string(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        An event raised when rw_u8_string is modified
        """
        return self.on_event(JD_PROTO_TEST_EV_E_U8_STRING, handler)


    def c_bool(self, bool: bool) -> None:
        """
        A command to set rw_bool.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_BOOL, bool)

    def c_u32(self, u32: int) -> None:
        """
        A command to set rw_u32.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_U32, u32)

    def c_i32(self, i32: int) -> None:
        """
        A command to set rw_i32.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_I32, i32)

    def c_string(self, string: str) -> None:
        """
        A command to set rw_string.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_STRING, string)

    def c_bytes(self, bytes: bytes) -> None:
        """
        A command to set rw_string.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_BYTES, bytes)

    def c_i8_u8_u16_i32(self, i8: int, u8: int, u16: int, i32: int) -> None:
        """
        A command to set rw_bytes.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_I8_U8_U16_I32, i8, u8, u16, i32)

    def c_u8_string(self, u8: int, string: str) -> None:
        """
        A command to set rw_u8_string.
        """
        self.send_cmd_packed(JD_PROTO_TEST_CMD_C_U8_STRING, u8, string)
    
