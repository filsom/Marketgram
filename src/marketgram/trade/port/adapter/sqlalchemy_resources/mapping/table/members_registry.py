from sqlalchemy.orm import registry, query_expression, relationship, composite
from sqlalchemy import event

from marketgram.trade.domain.model.p2p.paycard import Paycard
from marketgram.trade.domain.model.p2p.seller import Seller
from marketgram.trade.domain.model.p2p.user import User
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.members_table import (
    members_table
)


def members_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        Seller,
        members_table,
        properties={
            '_user_id': members_table.c.user_id,
            '_is_blocked': members_table.c.is_blocked,
            '_paycard': composite(
                Paycard, 
                members_table.c.first6,
                members_table.c.last4,
                members_table.c.synonym,
            ),
            '_balance': query_expression(),
        }
    )
    mapper.map_imperatively(
        User,
        members_table,
        properties={
            '_user_id': members_table.c.user_id,
            '_is_blocked': members_table.c.is_blocked,
            '_balance': query_expression(),
            '_entries': relationship(
                'PostingEntry',
                default_factory=list,
                lazy='noload'
            )
        }
    )


@event.listens_for(Seller, 'load')
def load_seller(seller, value):
    if seller._balance is None:
        seller._balance = Money(0)


@event.listens_for(User, 'load')
def load_user(user, value):
    if user._balance is None:
        user._balance = Money(0)