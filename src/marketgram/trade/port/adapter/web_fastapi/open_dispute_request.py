from uuid import UUID
from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.open_dispute_command import (
    OpenDisputeCommand,
    OpenDisputeHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class OpenDisputeRequest(BaseModel):
    deal_id: UUID


@router.post('/open_dispute')
async def dispute_closure_controller(
    field: OpenDisputeRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            OpenDisputeHandler
        )
        await handler.handle(
            OpenDisputeCommand(field.deal_id)
        )
        return 'OK'