from sqlalchemy.orm import registry, composite

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.category import Category
from marketgram.trade.domain.model.trade_item.type_category import TypeCategory
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.categories_table import (
    categories_table,
    category_types_table
)

def categories_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        TypeCategory,
        category_types_table,
        properties={
            'type_category_id': category_types_table.c.type_category_id,
            'name': category_types_table.c.category_types
        }
    )
    mapper.map_imperatively(
        Category,
        categories_table,
        properties={
            '_category_id': categories_table.c.category_id,
            '_service_id': categories_table.c.service_id,
            '_category_type_id': categories_table.c.category_type_id,
            '_alias': categories_table.c.alias,
            '_action_time': composite(
                ActionTime,
                categories_table.c.shipping_hours,
                categories_table.c.inspection_hours
            ),
            '_shipment': categories_table.c.shipment,
            '_minimum_price': composite(Money, categories_table.c.minimum_price),
            '_minimum_procent_discount': categories_table.c.minimum_procent_discount
        }
    )