from uuid import UUID

from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.product_quality_confirmation_command import (
    ProductQualityConfirmationCommand,
    ProductQualityConfirmationHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class ProductQualityConfirmationRequest(BaseModel):
    deal_id: UUID


@router.post('/product_quality')
async def product_quality_confirmation_controller(
    field: ProductQualityConfirmationRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        handler = await container.get(
            ProductQualityConfirmationHandler
        )
        await handler.handle(
            ProductQualityConfirmationCommand(field.deal_id)
        )
        return 'OK'