from uuid import UUID
from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.deal_cancellation_command import (
    DealCancellationCommand,
    DealCancellationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class DealCancellationRequest(BaseModel):
    deal_id: UUID


@router.post('/cancellation_deal')
async def deal_cancellation_controller(
    field: DealCancellationRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            DealCancellationHandler
        )
        await handler.handle(
            DealCancellationCommand(field.deal_id)
        )
        return 'OK'