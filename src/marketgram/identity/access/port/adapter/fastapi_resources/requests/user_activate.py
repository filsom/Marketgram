from fastapi import Request

from marketgram.common.application.handler import Handler
from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand, 
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


@router.get('/activate/{token}')
async def user_activate_controller(token: str, req: Request) -> str:
    async with Container(req) as container:
        handler = await container.get(
            Handler[UserAcivateCommand, None]
        )
        await handler.handle(
            UserAcivateCommand(token)
        )
        return 'OK'