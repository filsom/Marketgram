from fastapi import Request, Response

from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.forgot_password import (
    ForgotPasswordCommand, 
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


@router.post('/forgot_pwd')
async def forgot_password_controller(
    email: str, 
    req: Request, 
    res: Response
) -> str:
    async with Container(req) as container:
        # handler = await container.get(
        #     ForgotPasswordCommand, None]
        # )
        # await handler.handle(
        #     ForgotPasswordCommand(email)
        # )
        return 'OK'