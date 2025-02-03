from sqlalchemy.orm import registry, composite, relationship, column_property
from sqlalchemy import event

from marketgram.trade.domain.model.p2p.deal.overdue_deal import OverdueDeal
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
    mapper.map_imperatively(
        ShipDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_card_id': deals_table.c.card_id,
            '_members': relationship(
                'Members',
                lazy='selectin',
                uselist=False,
            ),
            '_qty_purchased': deals_table.c.qty_purchased,
            '_shipment': deals_table.c.shipment,
            '_price': composite(Money, deals_table.c.price),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.ship_to,
                deals_table.c.inspect_to,
            ),
            '_status': deals_table.c.status,
            '_created_at': deals_table.c.created_at,
            '_download_link': deals_table.c.download_link,
            '_shipped_at': deals_table.c.shipped_at,
        }
    )
    mapper.map_imperatively(
        ConfirmationDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_seller_id': column_property(deals_members_table.c.seller_id),
            '_price': composite(Money, deals_table.c.price),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.ship_to,
                deals_table.c.inspect_to,
            ),
            '_status': deals_table.c.status,
            '_inspected_at': deals_table.c.inspected_at,
            '_entries': relationship(
                'PostingEntry', 
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='noload',
                overlaps='_entries',
            )
        }
    )
    mapper.map_imperatively(
        CancellationDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_buyer_id': column_property(deals_members_table.c.buyer_id),
            '_price': composite(Money, deals_table.c.price),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.ship_to,
                deals_table.c.inspect_to,
            ),
            '_status': deals_table.c.status,
            '_entries': relationship(
                'PostingEntry', 
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='noload',
                overlaps='_entries',
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
                lazy='selectin',
                uselist=False,
                overlaps='_members',
            ),
            '_price': composite(Money, deals_table.c.price),
            '_deadlines': composite(
                Deadlines,
                deals_table.c.ship_to,
                deals_table.c.inspect_to,
            ),
            '_entries': relationship(
                'PostingEntry',
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='noload',
                overlaps='_entries,_entries',
            ),
            '_status': deals_table.c.status,
        }
    )
    mapper.map_imperatively(
        OverdueDeal,
        deals_table,
        properties={
            '_deal_id': deals_table.c.deal_id,
            '_members': relationship(
                'Members',
                lazy='selectin',
                uselist=False,
                overlaps='_members',
            ),
            '_price': composite(Money, deals_table.c.price),
            '_status': deals_table.c.status,
            '_entries': relationship(
                'PostingEntry', 
                secondary=deals_entries_table,
                uselist=True,
                default_factory=list,
                lazy='noload',
                overlaps='_entries',
            )
        }
    )


@event.listens_for(ShipDeal, 'load')
def load_user(deal, value):
    deal.events = []


@event.listens_for(CancellationDeal, 'load')
def load_user(deal, value):
    deal.events = []


@event.listens_for(ConfirmationDeal, 'load')
def load_user(deal, value):
    deal.events = []


@event.listens_for(DisputeDeal, 'load')
def load_user(deal, value):
    deal.events = []


@event.listens_for(OverdueDeal, 'load')
def load_user(deal, value):
    deal.events = []