from fastapi import Request, Response

from marketgram.common.port.adapter.container import Container
from marketgram.trade.application.commands.dispute_closure import (
    DisputeClosureCommand,
    DisputeClosureHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/dispute_closure')
async def dispute_closure_controller(
    deal_id: int, 
    req: Request, 
    res: Response
) -> str:
    async with Container(req, res) as container:
        handler = await container.get(
            DisputeClosureHandler
        )
        await handler.handle(
            DisputeClosureCommand(deal_id)
        )
        return 'OK'