from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.commands.card_buy import (
    CardBuyCommand,
    CardBuyHandler
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class CardBuyRequest(BaseModel):
    card_id: int
    qty: int
    price: str


@router.post('/buy_card')
async def card_buy_controller(
    field: CardBuyRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        command = CardBuyCommand(
            field.card_id,
            field.qty,
            field.price
        )
        handler = await container.get(
            CardBuyHandler
        )
        await handler.handle(command)

        return 'OK'