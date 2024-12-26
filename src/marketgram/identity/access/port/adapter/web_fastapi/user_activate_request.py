from fastapi import Request

from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.user_activate_command import (
    UserAcivateCommand, 
    UserActivateHandler
)


@router.get('/activate/{token}')
async def activate(token: str, req: Request) -> str:
    async with Container(req) as container:
        handler = await container.get(UserActivateHandler)
        await handler.handle(UserAcivateCommand(token))

        return 'OK'