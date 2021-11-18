# Autogenerated file. Do not edit.
from jacdac.bus import Bus, Client
from .constants import *
from typing import Optional, cast
from jacdac.events import EventHandlerFn, UnsubscribeFn

class WifiClient(Client):
    """
    Discovery and connection to WiFi networks. Separate TCP service can be used for data transfer.
     * 
     * The device controlled by this service is meant to connect automatically, once configured.
     * To that end, it keeps a list of known WiFi networks, with priorities and passwords.
     * It will connect to the available network with numerically highest priority,
     * breaking ties in priority by signal strength (typically all known networks have priority of `0`).
     * If the connection fails (due to wrong password, radio failure, or other problem)
     * an `connection_failed` event is emitted, and the device will try to connect to the next eligible network.
     * When networks are exhausted, the scan is performed again and the connection process restarts.
     * 
     * Updating networks (setting password, priorties, forgetting) does not trigger an automatic reconnect.
    """

    def __init__(self, bus: Bus, role: str) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_WIFI, JD_WIFI_PACK_FORMATS, role)
    

    @property
    def enabled(self) -> Optional[bool]:
        """
        Determines whether the WiFi radio is enabled. It starts enabled upon reset., 
        """
        reg = self.register(JD_WIFI_REG_ENABLED)
        values = reg.values()
        return cast(Optional[bool], values[0] if values else None)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        reg = self.register(JD_WIFI_REG_ENABLED)
        reg.set_values(value)


    @property
    def ip_address(self) -> Optional[bytes]:
        """
        0, 4 or 16 byte buffer with the IPv4 or IPv6 address assigned to device if any., 
        """
        reg = self.register(JD_WIFI_REG_IP_ADDRESS)
        values = reg.values()
        return cast(Optional[bytes], values[0] if values else None)

    @property
    def eui_48(self) -> Optional[bytes]:
        """
        The 6-byte MAC address of the device. If a device does MAC address randomization it will have to "restart"., 
        """
        reg = self.register(JD_WIFI_REG_EUI_48)
        values = reg.values()
        return cast(Optional[bytes], values[0] if values else None)

    @property
    def ssid(self) -> Optional[str]:
        """
        SSID of the access-point to which device is currently connected.
        Empty string if not connected., 
        """
        reg = self.register(JD_WIFI_REG_SSID)
        values = reg.values()
        return cast(Optional[str], values[0] if values else None)

    @property
    def rssi(self) -> Optional[int]:
        """
        Current signal strength. Returns -128 when not connected., _: dB
        """
        reg = self.register(JD_WIFI_REG_RSSI)
        values = reg.values()
        return cast(Optional[int], values[0] if values else None)

    def on_got_ip(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted upon successful join and IP address assignment.
        """
        return self.on_event(JD_WIFI_EV_GOT_IP, handler)

    def on_lost_ip(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when disconnected from network.
        """
        return self.on_event(JD_WIFI_EV_LOST_IP, handler)

    def on_scan_complete(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        A WiFi network scan has completed. Results can be read with the `last_scan_results` command.
        The event indicates how many networks where found, and how many are considered
        as candidates for connection.
        """
        return self.on_event(JD_WIFI_EV_SCAN_COMPLETE, handler)

    def on_networks_changed(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted whenever the list of known networks is updated.
        """
        return self.on_event(JD_WIFI_EV_NETWORKS_CHANGED, handler)

    def on_connection_failed(self, handler: EventHandlerFn) -> UnsubscribeFn:
        """
        Emitted when when a network was detected in scan, the device tried to connect to it
        and failed.
        This may be because of wrong password or other random failure.
        """
        return self.on_event(JD_WIFI_EV_CONNECTION_FAILED, handler)


    def add_network(self, ssid: str, password: str) -> None:
        """
        Automatically connect to named network if available. Also set password if network is not open.
        """
        self.send_cmd_packed(JD_WIFI_CMD_ADD_NETWORK, ssid, password)

    def reconnect(self, ) -> None:
        """
        Enable the WiFi (if disabled), initiate a scan, wait for results, disconnect from current WiFi network if any,
        and then reconnect (using regular algorithm, see `set_network_priority`).
        """
        self.send_cmd_packed(JD_WIFI_CMD_RECONNECT, )

    def forget_network(self, ssid: str) -> None:
        """
        Prevent from automatically connecting to named network in future.
        Forgetting a network resets its priority to `0`.
        """
        self.send_cmd_packed(JD_WIFI_CMD_FORGET_NETWORK, ssid)

    def forget_all_networks(self, ) -> None:
        """
        Clear the list of known networks.
        """
        self.send_cmd_packed(JD_WIFI_CMD_FORGET_ALL_NETWORKS, )

    def set_network_priority(self, priority: int, ssid: str) -> None:
        """
        Set connection priority for a network.
        By default, all known networks have priority of `0`.
        """
        self.send_cmd_packed(JD_WIFI_CMD_SET_NETWORK_PRIORITY, priority, ssid)

    def scan(self, ) -> None:
        """
        Initiate search for WiFi networks. Generates `scan_complete` event.
        """
        self.send_cmd_packed(JD_WIFI_CMD_SCAN, )
    
