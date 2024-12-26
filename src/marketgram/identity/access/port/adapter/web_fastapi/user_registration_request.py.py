from fastapi import Request
from pydantic import BaseModel

from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.user_registration_command import (
    UserRegistrationCommand, 
    UserRegistrationHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.routing import router


class UserRegistrationField(BaseModel):
    email: str
    password: str
    same_password: str


@router.post('/registration')
async def user_registration(
    field: UserRegistrationField, 
    req: Request
) -> str:
    async with Container(req) as container:
        command = UserRegistrationCommand(
            field.email,
            field.password,
            field.same_password
        )
        handler = await container.get(UserRegistrationHandler)
        await handler.handle(command)

        return 'OK'