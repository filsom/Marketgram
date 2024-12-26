from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.identity.access.application.forgot_password_coomand import (
    ForgotPasswordCommand, 
    ForgotPasswordHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.routing import router


@router.post('/forgot_pwd')
async def forgot_password(
    email: str, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(ForgotPasswordHandler)
        await handler.handle(ForgotPasswordCommand(email))

        return 'OK'