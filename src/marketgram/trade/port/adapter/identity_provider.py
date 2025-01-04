from uuid import UUID
from aiohttp import ClientSession

from fastapi import Request, Response


class AiohttpIdentityProvider:
    def __init__(
        self,
        request: Request,
        response: Response,
        client_session: ClientSession
    ):
        self._request = request
        self._response = response
        self._client_session = client_session

    def provided_id(self) -> UUID:
        return self._provided_id
    
    async def get_user_id(self) -> None:
        async with self._client_session.get(
            ...
        ) as response:
            json = await response.json()

            if response.start == 200:
                self._provided_id = ...
            else:
                raise