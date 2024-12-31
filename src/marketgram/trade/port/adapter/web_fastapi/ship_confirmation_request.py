from uuid import UUID

from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.ship_confirmation_command import (
    ShipConfirmationCommand,
    ShipConfirmationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class ShipConfirmationRequest(BaseModel):
    deal_id: UUID


@router.post('/ship_confirmation')
async def ship_confirmation_controller(
    field: ShipConfirmationRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            ShipConfirmationHandler
        )
        await handler.handle(
            ShipConfirmationCommand(field.deal_id)
        )
        return 'OK'