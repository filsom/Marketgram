from sqlalchemy.orm import registry, composite

from marketgram.trade.domain.model.trade_item1.card import Card
from marketgram.trade.domain.model.trade_item1.description import Description
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item1.sell_card import SellCard
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.cards_table import (
    cards_table
)


def cards_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        Card,
        cards_table,
        properties={
            '_card_id': cards_table.c.card_id,
            '_owner_id': cards_table.c.owner_id,
            '_price': composite(
                Money,
                cards_table.c.price
            ),
            '_description': composite(
                Description,
                cards_table.c.title,
                cards_table.c.text_description,
                cards_table.c.account_format,
                cards_table.c.region,
                cards_table.c.spam_block
            ),
            '_delivery': composite(
                Delivery,
                cards_table.c.format,
                cards_table.c.method,
            ),
            '_deadlines': composite(
                Deadlines,
                cards_table.c.shipping_hours,
                cards_table.c.receipt_hours,
                cards_table.c.check_hours,
            ),
            '_min_price': composite(
                Money,
                cards_table.c.min_price
            ),
            '_min_discount': cards_table.c.min_discount,
            '_created_at': cards_table.c.created_at,
            '_dirty_price': cards_table.c.dirty_price,
            '_is_archived': cards_table.c.is_archived,
            '_is_purchased': cards_table.c.is_purchased
        }
    )
    mapper.map_imperatively(
        SellCard,
        cards_table,
        properties={
            '_card_id': cards_table.c.card_id,
            '_owner_id': cards_table.c.owner_id,
            '_price': composite(
                Money,
                cards_table.c.price
            ),
            '_is_purchased': cards_table.c.is_purchased,
            '_created_at': cards_table.c.created_at,
            '_delivery': composite(
                Delivery,
                cards_table.c.format,
                cards_table.c.method,
            ),
            '_deadlines': composite(
                Deadlines,
                cards_table.c.shipping_hours,
                cards_table.c.receipt_hours,
                cards_table.c.check_hours,
            )
        }
    )