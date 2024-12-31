from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.trade.application.card_create_command import (
    CardCreateCommand, 
    CardCreateHandler
)
from marketgram.trade.domain.model.trade_item.description import (
    AccountFormat, 
    Region
)
from marketgram.trade.domain.model.p2p.format import Format
from marketgram.trade.domain.model.p2p.transfer_method import (
    TransferMethod
)
from marketgram.trade.port.adapter.web_fastapi.routing import router


class CardCreateRequest(BaseModel):
    amount: str
    title: str
    text_description: str
    account_format: AccountFormat
    region: Region
    spam_block: bool
    format: Format
    method: TransferMethod
    shipping_hours: int | None
    receipt_hours: int | None
    check_hours: int


@router.post('/card_create')
async def card_create_controller(
    field: CardCreateRequest, 
    req: Request, 
    res: Response
) -> str:
    async with RequestContainer(req, res) as container:
        command = CardCreateCommand(
            field.amount,
            field.title,
            field.text_description,
            field.account_format,
            field.region,
            field.spam_block,
            field.format,
            field.method,
            field.shipping_hours,
            field.receipt_hours,
            field.check_hours
        )
        handler = await container.get(
            CardCreateHandler
        )
        await handler.handle(command)

        return 'OK'