from uuid import UUID
from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.dispute_closure_command import (
    DisputeClosureCommand,
    DisputeClosureHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class DisputeClosureRequest(BaseModel):
    deal_id: UUID


@router.post('/dispute_closure')
async def dispute_closure_controller(
    field: DisputeClosureRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            DisputeClosureHandler
        )
        await handler.handle(
            DisputeClosureCommand(field.deal_id)
        )
        return 'OK'