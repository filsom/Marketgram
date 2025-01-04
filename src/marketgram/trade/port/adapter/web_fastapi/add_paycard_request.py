from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.commands.add_paycard import (
    AddPaycardCommand, 
    AddPaycardHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class AddPaycardRequest(BaseModel):
    first6: str
    last4: str
    synonym: str


@router.post('/add_paycard')
async def add_paycard_controller(
    field: AddPaycardRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        command = AddPaycardCommand(
            field.first6,
            field.last4,
            field.synonym
        )
        handler = await container.get(
            AddPaycardHandler
        )
        await handler.handle(command)

        return 'OK'
