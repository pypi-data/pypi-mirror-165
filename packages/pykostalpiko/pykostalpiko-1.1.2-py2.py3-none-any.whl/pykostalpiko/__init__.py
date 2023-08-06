"""Piko Inverter"""
import asyncio
import json
from base64 import b64encode
from hashlib import sha1
from multiprocessing.sharedctypes import Value
from types import TracebackType
from typing import Any, Optional, Type

from aiohttp import ClientSession

from pykostalpiko.dxs import find_descriptor_by_id
from pykostalpiko.dxs.entry import Descriptor


class Piko:
    """Piko Inverter API"""

    _session_id = None

    def __init__(
        self,
        client_session: ClientSession,
        host: str,
        username: str = "pvserver",
        password: str = "pvwr",
    ) -> None:
        """Constructor."""
        self._client_session = client_session
        self.host = host
        self.username = username
        self.password = password

    async def __aenter__(self) -> "Piko":
        await self.async_login()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.async_logout()

    async def async_login(self) -> None:
        """Get a logged in sessionId using the username and password"""

        # GET a sessionId and Salt for the sessionId
        async with self._client_session.get(
            f"http://{self.host}/api/login.json"
        ) as resp:
            # Sometimes the inverter doesn't respond with a salt and sessionId.
            # This just means that the login failed.
            try:
                resp_data = await resp.json(content_type="text/plain")
                salt = resp_data["salt"]
                session_id = resp_data["session"]["sessionId"]
            except KeyError as e:
                raise LoginException(
                    "The inverter doesn't provide a login session. Try again later."
                ) from e

        # Encrypt and encode the password with the salt
        password_sha1 = sha1((self.password + salt).encode("utf-8")).digest()
        password_encrypted = b64encode(password_sha1)

        login_body = {
            "mode": 1,
            "pwh": str(password_encrypted, "utf-8"),
            "userId": self.username,
        }

        # POST the sessionId, user and password to authorize the session
        async with self._client_session.post(
            f"http://{self.host}/api/login.json?sessionId={session_id}",
            data=json.dumps(login_body),
        ) as resp:
            resp_data = await resp.json(content_type="text/plain")

            # Check if the login was successful
            if resp_data["status"]["code"] != 0 or resp_data["session"]["roleId"] != 2:
                raise LoginException("Login failed")

            self._session_id = resp_data["session"]["sessionId"]

        return True

    async def async_logout(self) -> None:
        """Logout from the inverter."""
        async with self._client_session.get(
            f"http://{self.host}/api/logout.json"
        ) as resp:
            resp_data = await resp.json(content_type="text/plain")
            session_id = resp_data["session"]["sessionId"]

        if session_id != 0:
            raise LogoutException("Logout failed")

    async def _async_fetch(self, *entries: Descriptor) -> dict:
        """
        Fetch the data from the inverter
        Limited to 0 to 25 DXS entries
        """

        # Check amount of requested entries
        if len(entries) == 0:
            raise ValueError("No entries specified")
        if len(entries) > 25:
            raise ValueError("Too many entries specified")

        def _build_param(dxs: Descriptor) -> str:
            return f"dxsEntries={dxs.key}"

        params = map(_build_param, entries)
        url = f"http://{self.host}/api/dxs.json?" + "&".join(params)

        async with self._client_session.get(url) as response:
            json_body = await response.json(content_type="text/plain")
            return self._format_response(json_body)

    async def async_fetch_multiple(self, descriptors: list[Descriptor]) -> dict:
        """Fetch the data from the inverter."""

        # Spread the entries into groups of 25 to avoid too many dxsEntries
        entries_paged = [
            descriptors[i : i + 25] for i in range(0, len(descriptors), 25)
        ]

        data = {}

        for req in asyncio.as_completed(
            [self._async_fetch(*entries_page) for entries_page in entries_paged]
        ):
            res = await req

            if res is not None:
                # Combine existing data with newly fetched data
                data = {**data, **res}

        return data

    async def async_fetch(self, descriptor: Descriptor) -> Any:
        """Fetch the data from the inverter."""
        data = await self.async_fetch_multiple([descriptor])
        return data[descriptor.name]

    async def async_set_descriptors(
        self, descriptors: list[tuple[Descriptor, Any]]
    ) -> None:
        """Change the value of a configurable descriptor."""
        dxsEntries = []

        for descriptor, value in descriptors:
            # check if descriptor is set to be configurable
            if not descriptor.options.configurable:
                raise Exception(
                    f"Descriptor {descriptor.name} ({descriptor.key}) is not configurable"
                )

            dxsEntries.append({"dxsId": descriptor.key, "value": value})

        data = {"dxsEntries": dxsEntries}

        async with self._client_session.post(
            f"http://{self.host}/api/dxs.json?sessionId={self._session_id}",
            data=json.dumps(data),
        ) as response:
            json_body = await response.json(content_type="text/plain")

            if json_body["status"]["code"] != 0:
                raise Exception("An error occured setting the descriptors")

    @classmethod
    def _format_response(cls, response) -> dict[str, Any]:
        if response is None:
            return None

        new = {}
        entries = response["dxsEntries"]

        for entry in entries:
            value = entry["value"]
            if isinstance(value, float):
                value = round(value, 2)

            descriptor = find_descriptor_by_id(entry["dxsId"])

            if descriptor.options.multiplication_factor != 1:
                value = value * descriptor.options.multiplication_factor

            if descriptor.options.mapper_function is not None:
                value = descriptor.options.mapper_function(value)

            new[descriptor.name] = value

        return new


class LoginException(Exception):
    """Login exception"""


class LogoutException(Exception):
    """Logout exception"""
