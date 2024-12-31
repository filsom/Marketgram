from uuid import UUID

from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.receipt_confirmation_command import (
    ReceiptConfirmationHandler,
    ReceiptConfirmationCommand
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class ReceiptConfirmationRequest(BaseModel):
    deal_id: UUID


@router.post('/receipt_confirmation')
async def receipt_confirmation_controller(
    field: ReceiptConfirmationRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            ReceiptConfirmationHandler
        )
        await handler.handle(
            ReceiptConfirmationCommand(field.deal_id)
        )
        return 'OK'