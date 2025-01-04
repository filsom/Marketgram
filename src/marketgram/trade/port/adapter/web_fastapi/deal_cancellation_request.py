from fastapi import Request, Response

from marketgram.common.port.adapter.container import Container
from marketgram.trade.application.commands.deal_cancellation import (
    DealCancellationCommand,
    DealCancellationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/cancellation_deal')
async def deal_cancellation_controller(
    deal_id: int, 
    req: Request, 
    res: Response
) -> str:
    async with Container(req, res) as container:
        handler = await container.get(
            DealCancellationHandler
        )
        await handler.handle(
            DealCancellationCommand(deal_id)
        )
        return 'OK'