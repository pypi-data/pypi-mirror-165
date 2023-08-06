"""Class to represent a bulb attaches to a Zeptrion device"""

import logging
import aiohttp
from pyzeptrion.device import ZeptrionDevice
from pyzeptrion.const import (
    BULB_DIMDOWN,
    BULB_DIMUP,
    BULB_OFF,
    BULB_ON,
    OFF_STATE,
    ON_STATE,
)

_LOGGER = logging.getLogger(__name__)


class ZeptrionBulb(ZeptrionDevice):
    """A class for a Zeptrion bulb, derived from the ZetprionDevice class."""

    def __init__(
        self,
        host: str,
        chn: int,
        session: aiohttp.client.ClientSession = None,
    ):
        super().__init__(host, chn, session)

    @classmethod
    async def create(cls, self, host, chn):
        """Called before __init__ to assign values to the object"""
        self = ZeptrionBulb(host, chn)
        await self._set_description()
        self._state = await self.get_state()
        return self

    async def turn_on(self):
        """turn the bulb on and update state"""
        response = await self.request(
            uri=self._post_ctrl_uri, method="POST", data={"cmd": BULB_ON}
        )
        self._state = ON_STATE
        return response

    async def turn_off(self):
        """turn the bulb off and update state"""
        response = await self.request(
            uri=self._post_ctrl_uri, method="POST", data={"cmd": BULB_OFF}
        )
        self._state = OFF_STATE
        return response

    async def dim_down(self):
        """dim the bulb down"""
        response = await self.request(
            uri=self._post_ctrl_uri, method="POST", data={"cmd": BULB_DIMDOWN}
        )
        self._state = ON_STATE
        return response

    async def dim_up(self):
        """dim the bulp up"""
        response = await self.request(
            uri=self._post_ctrl_uri, method="POST", data={"cmd": BULB_DIMUP}
        )
        self._state = ON_STATE
        return response

    async def dim_down_t(self, t_milli: int):
        """dim the bulb down for t milliseconds"""
        if 100 <= t_milli <= 32000:
            response = await self.request(
                uri=self._post_ctrl_uri,
                method="POST",
                data={"cmd": BULB_DIMDOWN + "_(" + str(t_milli) + ")"},
            )
            self._state = ON_STATE
        return response

    async def dim_up_t(self, t_milli: int):
        """dim the bulb up for t milliseconds"""
        if 100 <= t_milli <= 32000:
            response = await self.request(
                uri=self._post_ctrl_uri,
                method="POST",
                data={"cmd": BULB_DIMUP + "_(" + str(t_milli) + ")"},
            )
            self._state = ON_STATE
        return response

    async def dim_t(self, t_milli: int):
        """dim the bulb in either direction for t milliseconds"""
        if 100 <= t_milli <= 32000:
            response = await self.request(
                uri=self._post_ctrl_uri,
                method="POST",
                data={"cmd": BULB_DIMUP + "_(" + str(t_milli) + ")"},
            )
            self._state = ON_STATE
        return response

    async def toggle(self):
        """toggle the bulb from on to off and vice-versa"""
        cmd = BULB_OFF if self._state == ON_STATE else BULB_ON
        response = await self.request(
            uri=self._post_ctrl_uri, method="POST", data={"cmd": cmd}
        )
        self._state = ON_STATE if cmd == BULB_ON else OFF_STATE
        return response

    # Session handling

    async def close(self) -> None:

        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "ZeptrionBulb":

        return self

    async def __aexit__(self, *exc_info) -> None:

        await self.close()
