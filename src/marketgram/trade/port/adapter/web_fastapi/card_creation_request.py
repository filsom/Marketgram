from fastapi import Request
from pydantic import BaseModel

from marketgram.trade.domain.model.description import AccountFormat, Region
from marketgram.trade.domain.model.p2p.format import Format
from marketgram.trade.domain.model.p2p.transfer_method import TransferMethod
from marketgram.trade.port.adapter.web_fastapi.routing import router


class CardCreationRequest(BaseModel):
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
async def card_creation(field: CardCreationRequest, request: Request):
    pass