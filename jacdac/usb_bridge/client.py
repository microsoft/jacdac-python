# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *



class UsbBridgeClient(Client):
    """
    This service is normally not announced or otherwise exposed on the serial bus.
     * It is used to communicate with a USB-Jacdac bridge at the USB layer.
     * The host sends broadcast packets to this service to control the link layer.
     * The device responds with broadcast reports (no-one else does that).
     * These packets are not forwarded to the UART Jacdac line.
     * 
     * Packets are sent over USB Serial (CDC).
     * The host shall set the CDC to 2Mbaud 8N1
     * (even though in some cases the USB interface is connected directly to the MCU and line settings are
     * ignored).
     * 
     * The CDC line carries both Jacdac frames and serial logging output.
     * Jacdac frames have valid CRC and are framed by delimeter characters and possibly fragmented.
     * 
     * `0xFE` is used as a framing byte.
     * Note that bytes `0xF8`-`0xFF` are always invalid UTF-8.
     * `0xFF` occurs relatively often in Jacdac packets, so is not used for framing.
     * 
     * The following sequences are supported:
     * 
     * * `0xFE 0xF8` - literal 0xFE
     * * `0xFE 0xF9` - reserved; ignore
     * * `0xFE 0xFA` - indicates that some serial logs were dropped at this point
     * * `0xFE 0xFB` - indicates that some Jacdac frames were dropped at this point
     * * `0xFE 0xFC` - Jacdac frame start
     * * `0xFE 0xFD` - Jacdac frame end
     * 
     * 0xFE followed by any other byte:
     * * in serial, should be treated as literal 0xFE (and the byte as itself, unless it's 0xFE)
     * * in frame data, should terminate the current frame fragment,
     *   and ideally have all data (incl. fragment start) in the current frame fragment treated as serial
    Implements a client for the `USB Bridge <https://microsoft.github.io/jacdac-docs/services/usbbridge>`_ service.

    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_USB_BRIDGE, JD_USB_BRIDGE_PACK_FORMATS, role)



    def disable_packets(self, ) -> None:
        """
        Disables forwarding of Jacdac packets.
        """
        self.send_cmd_packed(JD_USB_BRIDGE_CMD_DISABLE_PACKETS, )

    def enable_packets(self, ) -> None:
        """
        Enables forwarding of Jacdac packets.
        """
        self.send_cmd_packed(JD_USB_BRIDGE_CMD_ENABLE_PACKETS, )

    def disable_log(self, ) -> None:
        """
        Disables forwarding of serial log messages.
        """
        self.send_cmd_packed(JD_USB_BRIDGE_CMD_DISABLE_LOG, )

    def enable_log(self, ) -> None:
        """
        Enables forwarding of serial log messages.
        """
        self.send_cmd_packed(JD_USB_BRIDGE_CMD_ENABLE_LOG, )
    
