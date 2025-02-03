from sqlalchemy.orm import registry, relationship

from marketgram.trade.domain.model.trade_item.service import Service
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.categories_table import (
    categories_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.services_table import (
    services_table
)


def services_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        Service,
        services_table,
        properties={
            '_service_id': services_table.c.service_id,
            '_name': services_table.c.name,
            '_alias': services_table.c.alias,
            '_categories': relationship(
                'Category',
                secondary=categories_table,
                lazy='joined',
                default_factory=list
            )
        }
    )