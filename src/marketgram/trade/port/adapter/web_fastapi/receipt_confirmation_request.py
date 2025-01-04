from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.commands.receipt_confirmation import (
    ReceiptConfirmationHandler,
    ReceiptConfirmationCommand
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/receipt_confirmation')
async def receipt_confirmation_controller(
    deal_id: int, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            ReceiptConfirmationHandler
        )
        await handler.handle(
            ReceiptConfirmationCommand(deal_id)
        )
        return 'OK'