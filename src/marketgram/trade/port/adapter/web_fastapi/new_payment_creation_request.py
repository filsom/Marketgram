from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.new_payment_creation_command import (
    NewPaymentCreationCommand,
    NewPaymentCreationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/new_payment')
async def new_payment_creation_controller(
    amount: str, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            NewPaymentCreationHandler
        )
        await handler.handle(
            NewPaymentCreationCommand(amount)
        )
        return 'OK'