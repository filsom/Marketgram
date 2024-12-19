import asyncio
from datetime import datetime
from uuid import UUID
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.qty_purchased import QtyPurchased
from marketgram.trade.domain.model.p2p.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.in_memory_deals_repository import (
    InMemoryDealsRepository
)


SELLER_ID = UUID('07f7f246-65e3-4bcc-a77e-6d7ac976af48')
USER_ID = UUID('66780506-f02d-490a-8947-4c3801eadbb3')
DEAL_ID = UUID('783b21bc-bc2d-4776-81c8-900593c7b698')
CARD_ID = UUID('983b21bc-bc2d-4776-81c8-900593c7b698')

deal_repository = InMemoryDealsRepository()

async def test_create_deal():
    new_deal = ShipDeal(
        DEAL_ID,
        SELLER_ID,
        USER_ID,
        CARD_ID,
        QtyPurchased(1),
        TypeDeal.PROVIDING_CODE,
        datetime.now(),
        Money(200),
        TimeTags(datetime.now()),
        Deadlines(1, 1, 1),
        StatusDeal.NOT_SHIPPED
    )
    deal_repository.add(new_deal)

    assert await deal_repository.unshipped_with_id(SELLER_ID, DEAL_ID) is not None
    assert await deal_repository.unreceived_with_id(USER_ID, DEAL_ID) is None
    assert await deal_repository.unconfirmed_with_id(USER_ID, DEAL_ID) is None
    assert await deal_repository.not_disputed_with_id(USER_ID, DEAL_ID) is not None
    assert await deal_repository.disputed_with_id(DEAL_ID) is None
    assert await deal_repository.unclosed_with_id(SELLER_ID, DEAL_ID) is not None


async def test_confirmation_shipment():
    exists_deal = await deal_repository.unshipped_with_id(
        SELLER_ID, 
        DEAL_ID
    )
    current_date = datetime.now()
    exists_deal.confirm_shipment(current_date)
    
    assert exists_deal._time_tags.shipped_at == TimeTags(exists_deal._time_tags.created_at, current_date, current_date)
    assert exists_deal._time_tags.received_at == current_date
    assert exists_deal._status == StatusDeal.CHECK


async def main():
    await test_create_deal()
    await test_confirmation_shipment()

if __name__ == '__main__':
    asyncio.run(main())