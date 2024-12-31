from uuid import UUID
from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.discount_setting_command import (
    DiscountSettingCommand,
    DiscountSettingHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class DiscountSettingRequest(BaseModel):
    card_id: UUID
    amount: str


@router.post('/discount_setting')
async def discount_setting_controller(
    field: DiscountSettingRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        command = DiscountSettingCommand(
            field.card_id,
            field.amount
        )
        handler = await container.get(
            DiscountSettingHandler
        )
        await handler.handle(command)

        return 'OK'