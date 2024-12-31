from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.payout_creation_command import (
    PayoutCreationCommand,
    PayoutCreationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class PayoutCreationRequest(BaseModel):
    amount: str


@router.post('/new_payout')
async def payout_creation_controller(
    field: PayoutCreationRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            PayoutCreationHandler
        )
        await handler.handle(
            PayoutCreationCommand(field.amount)
        )
        return 'OK'