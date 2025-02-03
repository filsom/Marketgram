from sqlalchemy.orm import registry, composite, column_property, relationship
from sqlalchemy import case, event, func, select

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.editable_card import EditableCard
from marketgram.trade.domain.model.trade_item.moderation_card import ModerationCard
from marketgram.trade.domain.model.trade_item.purchased_card import PurchasedCard
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.trade_item.sell_stock_card import SellStockCard
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.inventory_entries_table import (
    inventory_entries_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.cards_table import (
    cards_table,
    cards_descriptions_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.categories_table import (
    categories_table
)


def cards_registry_mapper(mapper: registry) -> None:
    sell_card_mapper = mapper.map_imperatively(
        SellCard,
        cards_table,
        polymorphic_on=case(
            (cards_table.c.shipment == Shipment.CHAT, Shipment.HAND),
            else_=Shipment.HAND
        ),
        polymorphic_identity=Shipment.HAND,
        properties={
            '_card_id': cards_table.c.card_id,
            '_owner_id': cards_table.c.owner_id,
            '_price': composite(Money,cards_table.c.price),
            '_shipment': cards_table.c.shipment,
            '_action_time': composite(
                ActionTime,
                cards_table.c.shipping_hours,
                cards_table.c.inspection_hours
            ),
            '_status': cards_table.c.status
        }
    )
    mapper.map_imperatively(
        SellStockCard,
        None,
        inherits=sell_card_mapper,
        polymorphic_identity=Shipment.AUTO,
        properties={
            '_stock_balance': column_property(
                select(func.sum(inventory_entries_table))
                .where(inventory_entries_table.c.card_id == cards_table.c.card_id)
                .scalar_subquery()
            ),
            '_inventory_entries': relationship(
                'InventoryEntry',
                secondary=inventory_entries_table,
                lazy='noload',
                default_factory=list
            )
        }
    )
    mapper.map_imperatively(
        ModerationCard,
        cards_table,
        properties={
            '_card_id': cards_table.c.card_id,
            '_owner_id': cards_table.c.owner_id,
            '_category_id': cards_table.c.category_id,
            '_price': composite(Money, cards_table.c.price),
            '_init_price': composite(Money, cards_table.c.price),
            '_descriptions': relationship(
                'Description',
                secondary=cards_descriptions_table,
                primaryjoin="and_(Description.status.in_(['new', 'current']))",
            ),
            '_features': cards_table.c.features,
            '_action_time': composite(
                ActionTime,
                cards_table.c.shipping_hours,
                cards_table.c.inspection_hours
            ),
            '_shipment': cards_table.c.shipment,
            '_created_at': cards_table.c.created_at,
            '_status': cards_table.c.status
        }
    )
    mapper.map_imperatively(
        EditableCard,
        cards_table,
        properties={
            '_card_id': cards_table.c.card_id,
            '_price': composite(Money, cards_table.c.price),
            '_init_price': composite(Money, cards_table.c.price),
            '_action_time': composite(
                ActionTime,
                cards_table.c.shipping_hours,
                cards_table.c.inspection_hours
            ),
            '_shipment': cards_table.c.shipment,
            '_minimum_price': column_property(categories_table.c.minimum_price),
            '_minimum_procent_discount': column_property(categories_table.c.minimum_procent_discount),
            '_status': cards_table.c.status,
            '_descriptions': relationship(
                'Description',
                secondary=cards_descriptions_table,
                primaryjoin="and_(Description.status.in_(['new', 'current']))",
            ),
        }
    )
    mapper.map_imperatively(
        PurchasedCard,
        cards_table,
        properties={
            '_card_id': cards_table.c.card_id,
            '_owner_id': cards_table.c.owner_id,
            '_category_id': cards_table.c.category_id,
            '_price': composite(Money, cards_table.c.price),
            '_descriptions': relationship(
                'Description',
                secondary=cards_descriptions_table,
                primaryjoin="and_(Description.status.in_(['new', 'current']))",
            ),
            '_features': cards_table.c.features,
            '_action_time': composite(
                ActionTime,
                cards_table.c.shipping_hours,
                cards_table.c.inspection_hours
            ),
            '_shipment': cards_table.c.shipment,
            '_created_at': cards_table.c.created_at,
            '_status': cards_table.c.status,
        }
    )
    



@event.listens_for(SellCard, 'load')
def load_user(card, value):
    card.events = []


@event.listens_for(SellStockCard, 'load')
def load_user(card, value):
    if card._stock_balance is None:
        card._stock_balance = 0
        
    card.events = []