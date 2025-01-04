from fastapi import Request
from pydantic import BaseModel

from marketgram.common.application.handler import Handler
from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationCommand, 
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


class UserRegistrationField(BaseModel):
    email: str
    password: str
    same_password: str


@router.post('/registration')
async def user_registration_controller(
    field: UserRegistrationField, 
    req: Request
) -> str:
    async with Container(req) as container:
        command = UserRegistrationCommand(
            field.email,
            field.password,
            field.same_password
        )
        handler = await container.get(
            Handler[UserRegistrationCommand, None]
        )
        await handler.handle(command)

        return 'OK'