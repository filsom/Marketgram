from fastapi import Request

from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand, 
    UserActivateHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.routing import router


@router.get('/activate/{token}')
async def user_activate_controller(token: str, req: Request) -> str:
    async with Container(req) as container:
        handler = await container.get(UserActivateHandler)
        await handler.handle(UserAcivateCommand(token))

        return 'OK'