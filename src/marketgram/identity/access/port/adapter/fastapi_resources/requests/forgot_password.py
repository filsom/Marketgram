from fastapi import Request, Response

from marketgram.common.application.handler import Handler
from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.forgotten_password import (
    ForgottenPasswordCommand, 
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


@router.post('/forgot_pwd')
async def forgot_password_controller(
    email: str, 
    req: Request, 
    res: Response
) -> str:
    async with Container(req) as container:
        handler = await container.get(
            Handler[ForgottenPasswordCommand, None]
        )
        await handler.handle(
            ForgottenPasswordCommand(email)
        )
        return 'OK'