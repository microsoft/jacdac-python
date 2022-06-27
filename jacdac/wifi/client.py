# Autogenerated file. Do not edit.
from jacdac.bus import Bus, SensorClient, EventHandlerFn, UnsubscribeFn
from .constants import *
from typing import Optional


class WifiClient(SensorClient):
    """
    Discovery and connection to WiFi networks. Separate TCP service can be used for data transfer.
    Implements a client for the `WIFI <https://microsoft.github.io/jacdac-docs/services/wifi>`_ service.

    """

    def __init__(self, bus: Bus, role: str, *, missing_rssi_value: Optional[int] = None) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_WIFI, JD_WIFI_PACK_FORMATS, role)
        self.missing_rssi_value = missing_rssi_value

    @property
    def rssi(self) -> Optional[int]:
        """
        Current signal strength. Returns -128 when not connected., _: dB
        """
        self.refresh_reading()
        return self.register(JD_WIFI_REG_RSSI).value(self.missing_rssi_value)

    @property
    def enabled(self) -> Optional[bool]:
        """
        Determines whether the WiFi radio is enabled. It starts enabled upon reset., 
        """
        return self.register(JD_WIFI_REG_ENABLED).bool_value()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.register(JD_WIFI_REG_ENABLED).set_values(value)


    @property
    def ip_address(self) -> Optional[bytes]:
        """
        0, 4 or 16 byte buffer with the IPv4 or IPv6 address assigned to device if any., 
        """
        return self.register(JD_WIFI_REG_IP_ADDRESS).value()

    @property
    def eui_48(self) -> Optional[bytes]:
        """
        The 6-byte MAC address of the device. If a device does MAC address randomization it will have to "restart"., 
        """
        return self.register(JD_WIFI_REG_EUI_48).value()

    @property
    def ssid(self) -> Optional[str]:
        """
        SSID of the access-point to which device is currently connected.
        Empty string if not connected., 
        """
        return self.register(JD_WIFI_REG_SSID).value()

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
    
