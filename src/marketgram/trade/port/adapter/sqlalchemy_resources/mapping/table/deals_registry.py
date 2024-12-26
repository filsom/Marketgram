from sqlalchemy.orm import registry, composite, relationship

from marketgram.trade.domain.model.p2p.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.receipt_deal import ReceiptDeal
from marketgram.trade.domain.model.p2p.ship_deal import (
    ShipDeal, 
    ShipLoginCodeDeal, 
    ShipProvidingLinkDeal
)
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.p2p.user import QuantityPurchased
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_table, 
    deals_entries_table
)


def deals_registry_mapper(mapper: registry) -> None:
    ship_deal_mapper = mapper.map_imperatively(
        ShipDeal,
        deals_table,
        polymorphic_on=deals_table.c.type,
        polymorphic_identity=TypeDeal.AUTO_LINK,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_seller_id': deals_table.c.seller_id,
            '_buyer_id': deals_table.c.buyer_id,
            '_card_id': deals_table.c.card_id,
            '_qty_purchased': composite(
                QuantityPurchased,
                deals_table.c.qty_purchased
            ),
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
            '_buyer_id': deals_table.c.buyer_id,
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
                lazy='subquery',
                overlaps='_entries'
            )
        }
    )
    mapper.map_imperatively(
        DisputeDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_buyer_id': deals_table.c.buyer_id,
            '_seller_id': deals_table.c.seller_id,
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
                lazy='subquery',
                overlaps='_entries,_entries'
            ),
            '_payout': relationship(
                'Payout',
                primaryjoin='and_('
                    'foreign(DisputeDeal._seller_id)==Payout._user_id, '
                    'Payout._is_processed==False'
                ')',
                uselist=False,
                lazy='noload',
                default_factory=list,
            )
        }
    )