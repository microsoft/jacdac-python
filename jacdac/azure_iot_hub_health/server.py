import asyncio
from typing import Optional, Union, cast
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

from jacdac.pack import jdpack

from ..bus import Bus, Server
from ..packet import JDPacket
from .constants import *

CONNECTION_STRING_FILE = "./.jacdac/iothub.txt"


class AzureIotHubHealthServer(Server):
    """A Azure IoT Hub Health server

    This server uses the 'azure-iot-device' PyPi package

    pip install azure-iot-device
    """

    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_AZURE_IOT_HUB_HEALTH)
        self.device_client: Optional[IoTHubDeviceClient] = None
        self._connection_status = AzureIotHubHealthConnectionStatus.DISCONNECTED
        asyncio.create_task(self.connect())

    async def send_message(self, msg: Union[str, Message]):
        self.debug("send message")
        self._check_connection()
        if self.connection_status == AzureIotHubHealthConnectionStatus.DISCONNECTED:
            await self.connect()

        if self.connection_status == AzureIotHubHealthConnectionStatus.CONNECTED:
            try:
                await self.device_client.send_message(msg)  # type: ignore
                self.send_event(JD_AZURE_IOT_HUB_HEALTH_EV_MESSAGE_SENT)
            except Exception as e:
                print(e)
                self.error("send message error")
                await self.disconnect()

    @property
    def connection_status(self) -> AzureIotHubHealthConnectionStatus:
        return self._connection_status

    @connection_status.setter
    def connection_status(self, value: AzureIotHubHealthConnectionStatus):
        if self._connection_status != value:
            self._connection_status = value
            self.send_event(JD_AZURE_IOT_HUB_HEALTH_EV_CONNECTION_STATUS_CHANGE, jdpack(
                JD_AZURE_IOT_HUB_HEALTH_PACK_FORMATS[JD_AZURE_IOT_HUB_HEALTH_EV_CONNECTION_STATUS_CHANGE], self._connection_status))

    def _check_connection(self):
        if self.connection_status == AzureIotHubHealthConnectionStatus.CONNECTED and not self.device_client.connected:  # type: ignore
            self.connection_status = AzureIotHubHealthConnectionStatus.DISCONNECTED

    async def connect(self):
        if self.device_client:
            await self.disconnect()

        self.debug("connect")
        self.connection_status = AzureIotHubHealthConnectionStatus.CONNECTING
        try:
            with open(CONNECTION_STRING_FILE, "r") as f:
                conn_str = f.read()
                self.device_client = IoTHubDeviceClient.create_from_connection_string(  # type: ignore
                    conn_str)
                await self.device_client.connect()
            self.connection_status = AzureIotHubHealthConnectionStatus.CONNECTED
        except Exception as e:
            self.error("connect failed {}", e)
            self.connection_status = AzureIotHubHealthConnectionStatus.DISCONNECTED

    def set_connection_string(self, conn_str: str):
        self.debug("set connection string")
        with open(CONNECTION_STRING_FILE, "w") as f:
            f.write(conn_str)

    async def disconnect(self):
        if not self.device_client:
            return

        self.debug("disconnect")
        self.connection_status = AzureIotHubHealthConnectionStatus.DISCONNECTING
        try:
            await self.device_client.shutdown()
        except Exception as e:
            self.debug("connect failed {}", e)
        finally:
            self.device_client = None
            self.connection_status = AzureIotHubHealthConnectionStatus.DISCONNECTED

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command

        if cmd == JD_GET(JD_AZURE_IOT_HUB_HEALTH_REG_HUB_NAME):
            self.send_report(pkt.not_implemented())
        elif cmd == JD_GET(JD_AZURE_IOT_HUB_HEALTH_REG_HUB_DEVICE_ID):
            self.send_report(pkt.not_implemented())
        elif cmd == JD_GET(JD_AZURE_IOT_HUB_HEALTH_REG_CONNECTION_STATUS):
            self.send_report(JDPacket.packed(
                cmd, JD_AZURE_IOT_HUB_HEALTH_PACK_FORMATS[JD_AZURE_IOT_HUB_HEALTH_REG_CONNECTION_STATUS], self.connection_status))
        elif cmd == JD_AZURE_IOT_HUB_HEALTH_CMD_CONNECT:
            self.handle_connect(pkt)
        elif cmd == JD_AZURE_IOT_HUB_HEALTH_CMD_DISCONNECT:
            self.handle_disconnect(pkt)
        elif cmd == JD_AZURE_IOT_HUB_HEALTH_CMD_SET_CONNECTION_STRING:
            self.handle_set_connection_string(pkt)

        return super().handle_packet(pkt)

    def handle_connect(self, pkt: JDPacket):
        self.debug("connect requested")
        asyncio.create_task(self.connect())

    def handle_disconnect(self, pkt: JDPacket):
        self.debug("disconnect requested")
        asyncio.create_task(self.disconnect())

    def handle_set_connection_string(self, pkt: JDPacket):
        [conn_str] = pkt.unpack("s")
        self.set_connection_string(cast(str, conn_str))
