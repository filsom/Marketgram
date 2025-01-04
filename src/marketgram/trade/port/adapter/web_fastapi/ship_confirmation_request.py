from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.commands.ship_confirmation import (
    ShipConfirmationCommand,
    ShipConfirmationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/ship_confirmation')
async def ship_confirmation_controller(
    deal_id: int, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            ShipConfirmationHandler
        )
        await handler.handle(
            ShipConfirmationCommand(deal_id)
        )
        return 'OK'