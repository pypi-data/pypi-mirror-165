"""Base class for the representation of Zeptrion devices"""
import asyncio
import hashlib
import socket
from typing import Any, Mapping, Optional
import xml.etree.ElementTree as ET
import async_timeout
import aiohttp
import pkg_resources
from yarl import URL
from .exceptions import ZeptrionConnectionError
from .const import (
    device_types,
    GET_STATE_URL,
    GET_DESC_URL,
    POST_CTRL_URL,
    TIMEOUT,
    OFF_STATE,
    ON_STATE,
)

__version__ = pkg_resources.get_distribution("setuptools").version
USER_AGENT = f"PythonZeptrion/{__version__}"


class ZeptrionDevice(object):
    """Base class for all Zeptrion devices (Bulb, blind)."""

    def __init__(self, host, chn, session):

        self._close_session = False
        self._session = session
        self._host = host
        self._chn = chn

        """ Build the different needed URLs"""
        self._get_desc_uri = URL(
            str(URL.build(scheme="http", host=self._host, path=GET_DESC_URL))
            + str(self._chn)
        )
        self._get_state_uri = URL(
            str(URL.build(scheme="http", host=self._host, path=GET_STATE_URL))
            + str(self._chn)
        )
        self._post_ctrl_uri = URL(
            str(URL.build(scheme="http", host=self._host, path=POST_CTRL_URL))
            + str(self._chn)
            + "/"
        )

        """ Additional variables to represent the device """
        self._name = None
        self._group = None
        self._state = False
        self._dev_type = None
        self._dev_id = None

    async def _set_description(self) -> object:
        """Set the additional variables by getting the description form the devices"""
        response = await self.request(uri=self._get_desc_uri, method="GET")
        base = ET.fromstring(response)
        self._name = base.find("name").text
        self._group = base.find("group").text
        self._dev_type = device_types[base.find("cat").text]

        # Generate a unique ID form the host and chn variables
        id_hash = hashlib.sha1()
        id_hash.update(str(self._name + self._host + str(self._chn)).encode("utf-8"))
        self._dev_id = id_hash.hexdigest()

    async def get_state(self) -> object:
        """Get the actual state of the device and set the variable"""
        response = await self.request(
            uri=self._get_state_uri,
            method="GET",
        )
        mybase = ET.fromstring(response)
        print("state:", (mybase[0][0].text))
        mystate = ON_STATE if int(mybase[0][0].text) > 0 else OFF_STATE
        return mystate

    async def post_cmd(self, cmd):
        """Generic call to change the state of any devices"""
        response = await self.request(
            uri=self._post_ctrl_uri, method="POST", data={"cmd": cmd}
        )
        self._state = cmd
        return response

    @property
    def state(self) -> Optional[str]:
        """Access to protected variable"""
        return self._state

    @property
    def name(self) -> Optional[str]:
        """Access to protected variable"""
        return self._name

    @property
    def group(self) -> Optional[str]:
        """Access to protected variable"""
        return self._group

    @property
    def chn(self) -> Optional[str]:
        """Access to protected variable"""
        return self._chn

    @property
    def host(self) -> Optional[str]:
        """Access to protected variable"""
        return self._host

    @property
    def type(self) -> Optional[str]:
        """Access to protected variable"""
        return self._dev_type

    @property
    def dev_id(self) -> Optional[str]:
        """Access to protected variable"""
        return self._dev_id

    def __str__(self):
        return f"Host: {self._host}\nChannel: {self._chn}\nName: {self._name}\nGroup: {self._group}\nState: {self._state}\nType: {self._dev_type}\nID:{self._dev_id}\n\n"

    def __del__(self):
        pass

    async def request(
        self,
        uri: str,
        method: str,
        data: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Async http request"""
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(TIMEOUT):
                response = await self._session.request(
                    method, uri, data=data, params=params, headers=headers
                )
        except asyncio.TimeoutError as exception:
            raise ZeptrionConnectionError(
                "Timeout occurred while connecting to Zeptrion device."
            ) from exception

        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ZeptrionConnectionError(
                "Error occurred while communicating with Zeptrion device."
            ) from exception

        text = await response.text()
        return text

    # Session handling

    async def close(self) -> None:
        """close sessions"""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "ZeptrionDevice":

        return self

    async def __aexit__(self, *exc_info) -> None:

        await self.close()
