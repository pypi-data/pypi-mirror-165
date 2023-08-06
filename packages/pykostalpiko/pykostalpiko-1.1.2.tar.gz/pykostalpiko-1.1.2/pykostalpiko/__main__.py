"""Simple cli tool to read the kostal piko data."""
import asyncio
import sys

from aiohttp import ClientSession

from pykostalpiko import Piko
from pykostalpiko.dxs.current_values import LIST_ALL


def main():
    """Run the asyncio main function."""
    asyncio.run(asnyc_main())


async def asnyc_main():
    """Request the current values from the piko inverter using the username and password"""

    user = {}

    if len(sys.argv) == 4:
        user = {"username": sys.argv[2], "password": sys.argv[3]}

    async with ClientSession() as session:
        async with Piko(session, sys.argv[1], **user) as piko:
            print(await piko.async_fetch_multiple(LIST_ALL))


if __name__ == "__main__":
    main()
