""" Classes to discover Zeptrion devices in the local network"""
import logging
import asyncio
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf
from pyzeptrion.bulb import ZeptrionBulb


_TIMEOUT_MS = 3000

logger = logging.getLogger(__name__)


class ZeptrionZeroconfListener(object):
    """Class to search the local network for Zeptrion devices using the zeroconf protocol"""

    def __init__(self) -> None:
        """Init the listener."""
        self.data = []

    def remove_service(self, name):
        """remove a sevice"""
        print(f"Service ({name} removed")

    def add_service(self, zeroconf, zeroconf_type, name):
        """Add a device that became visible via zeroconf."""
        asyncio.ensure_future(self.async_add_service(zeroconf, zeroconf_type, name))

    async def async_add_service(self, zeroconf, zeroconf_type, name):
        """Add a device that became visible via zeroconf."""
        info = AsyncServiceInfo(zeroconf_type, name)
        await info.async_request(zeroconf, _TIMEOUT_MS)
        self.data.append(info)

    update_service = add_service

    def get_data(self):
        """return the data"""
        return self.data


class ZeptrionRegistryDevice(object):
    """Representation of a device in the registry"""

    def __init__(self, host: str, chn: int, dev_type: str):
        self._host = host
        self._chn = chn
        self._dev_type = dev_type

    def __str__(self):
        return f"Host: {self._host}\nChannel: {self._chn}\ndev_type: {self._dev_type}\n"

    @property
    def host(self) -> str:
        """protected access to self._host"""
        return self._host

    @property
    def chn(self) -> int:
        """protected access to self._chn"""
        return self._chn

    @property
    def dev_type(self) -> str:
        """protected access to self._dev_type"""
        return self._dev_type


class ZeptrionRegistry(object):
    """Class to built a registry of Zeptrion devices"""

    def __init__(self):
        self._devices = []

    @classmethod
    async def create_registry(cls, self):
        """create the registry before __init__."""
        my_async_zeroconf = AsyncZeroconf()
        listener = ZeptrionZeroconfListener()
        service_browser = AsyncServiceBrowser(
            my_async_zeroconf.zeroconf, "_zapp._tcp.local.", listener
        )
        await asyncio.sleep(5)
        self.devices = []

        try:
            for info in listener.get_data():
                host = info.parsed_addresses()[0]
                channels = str(info.properties[b"type"]).split("-")[1]
                for chn in range(int(channels)):
                    temp_device = await ZeptrionBulb.create(
                        ZeptrionBulb, host, str(chn + 1)
                    )
                    if temp_device.dev_type != "NaN":
                        device = ZeptrionRegistryDevice(
                            host, chn + 1, temp_device.dev_type
                        )
                        self.devices.append(device)
                    await temp_device.close()
                    del temp_device

        finally:
            await service_browser.async_cancel()
            if not my_async_zeroconf:
                await my_async_zeroconf.close()

        self.devices.sort(key=lambda x: x.dev_type)
        return self

    @property
    def devices(self):
        """access to protected self._devices."""
        return self._devices
