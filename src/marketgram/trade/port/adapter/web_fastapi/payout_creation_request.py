from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.commands.payout_creation import (
    PayoutCreationCommand,
    PayoutCreationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/new_payout')
async def payout_creation_controller(
    amount: str, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            PayoutCreationHandler
        )
        await handler.handle(
            PayoutCreationCommand(amount)
        )
        return 'OK'