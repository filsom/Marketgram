from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.open_dispute_command import (
    OpenDisputeCommand,
    OpenDisputeHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/open_dispute')
async def dispute_closure_controller(
    deal_id: int, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            OpenDisputeHandler
        )
        await handler.handle(
            OpenDisputeCommand(deal_id)
        )
        return 'OK'