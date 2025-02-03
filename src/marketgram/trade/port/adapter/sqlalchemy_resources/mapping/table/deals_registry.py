from sqlalchemy.orm import registry, composite, relationship, column_property

from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.deal.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_table, 
    deals_entries_table,
    deals_members_table
)


def deals_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        Members,
        deals_members_table,
        properties={
            'seller_id': deals_members_table.c.seller_id,
            'buyer_id': deals_members_table.c.buyer_id
        }
    )
    ship_deal_mapper = mapper.map_imperatively(
        ShipDeal,
        deals_table,
        polymorphic_on=deals_table.c.type,
        polymorphic_identity=TypeDeal.AUTO,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_members': relationship(
                'Members',
                lazy='joined',
                uselist=False,
            ),
            '_card_id': deals_table.c.card_id,
            '_qty_purchased': deals_table.c.qty_purchased,
            '_type_deal': deals_table.c.type,
            '_price': composite(Money, deals_table.c.price),
            '_card_created_at': deals_table.c.card_created_at,
            '_time_tags': composite(
                TimeTags,
                deals_table.c.created_at,
                deals_table.c.shipped_at,
                deals_table.c.received_at,
                deals_table.c.closed_at
            ),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.shipping_hours,
                deals_table.c.receipt_hours,
                deals_table.c.check_hours,
            ),
            '_status': deals_table.c.status,
        }
    )
    mapper.map_imperatively(
        ShipLoginCodeDeal,
        None,
        inherits=ship_deal_mapper,
        polymorphic_identity=TypeDeal.PROVIDING_CODE,
    )
    mapper.map_imperatively(
        ShipProvidingLinkDeal,
        None,
        inherits=ship_deal_mapper,
        polymorphic_identity=TypeDeal.PROVIDING_LINK,
    )
    mapper.map_imperatively(
        ConfirmationDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_card_created_at': deals_table.c.card_created_at,
            '_time_tags': composite(
                TimeTags,
                deals_table.c.created_at,
                deals_table.c.shipped_at,
                deals_table.c.received_at,
                deals_table.c.closed_at
            ),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.shipping_hours,
                deals_table.c.receipt_hours,
                deals_table.c.check_hours,
            ),
            '_status': deals_table.c.status,
            '_entries': relationship(
                'PostingEntry', 
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='noload',
                overlaps='_entries'
            )
        }
    )
    mapper.map_imperatively(
        ReceiptDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_time_tags': composite(
                TimeTags,
                deals_table.c.created_at,
                deals_table.c.shipped_at,
                deals_table.c.received_at,
                deals_table.c.closed_at
            ),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.shipping_hours,
                deals_table.c.receipt_hours,
                deals_table.c.check_hours,
            ),
            '_status': deals_table.c.status,
        }
    )
    mapper.map_imperatively(
        CancellationDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_buyer_id': column_property(deals_members_table.c.buyer_id),
            '_price': composite(Money, deals_table.c.price),
            '_time_tags': composite(
                TimeTags,
                deals_table.c.created_at,
                deals_table.c.shipped_at,
                deals_table.c.received_at,
                deals_table.c.closed_at
            ),
            '_status': deals_table.c.status,
            '_entries': relationship(
                'PostingEntry', 
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='joined',
                overlaps='_entries'
            )
        }
    )
    mapper.map_imperatively(
        DisputeDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_members': relationship(
                'Members',
                lazy='joined',
                uselist=False,
                overlaps='_members'
            ),
            '_price': composite(Money, deals_table.c.price),
            '_is_disputed': deals_table.c.is_disputed,
            '_time_tags': composite(
                TimeTags,
                deals_table.c.created_at,
                deals_table.c.shipped_at,
                deals_table.c.received_at,
                deals_table.c.closed_at
            ),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.shipping_hours,
                deals_table.c.receipt_hours,
                deals_table.c.check_hours,
            ),
            '_status': deals_table.c.status,
            '_deal_entries': relationship(
                'PostingEntry',
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='joined',
                overlaps='_entries,_entries'
            ),
        }
    )