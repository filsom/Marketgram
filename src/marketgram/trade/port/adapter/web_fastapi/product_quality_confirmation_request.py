from fastapi import Request, Response

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.product_quality_confirmation_command import (
    ProductQualityConfirmationCommand,
    ProductQualityConfirmationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


@router.post('/product_quality')
async def product_quality_confirmation_controller(
    deal_id: int, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            ProductQualityConfirmationHandler
        )
        await handler.handle(
            ProductQualityConfirmationCommand(deal_id)
        )
        return 'OK'