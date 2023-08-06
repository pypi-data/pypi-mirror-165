from typing import (
    NoReturn,
    Optional,
)
from typing_extensions import Self

from aiohttp import ClientSession

try:
    import ujson as json
except ImportError:
    import json


class Enka(object):
    _client: Optional[ClientSession] = None

    async def __aenter__(self) -> Self:
        if self._client is None:
            self._client = ClientSession(json_serialize=json.dumps)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        if not (self._client is None or self._client.closed):
            await self._client.close()

    async def fetch(self, uid: int):
        ...
