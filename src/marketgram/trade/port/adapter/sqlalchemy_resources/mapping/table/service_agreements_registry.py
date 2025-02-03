from sqlalchemy.orm import registry

from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.service_agreements_table import (
    service_agreements_table
)


def service_agreements_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        ServiceAgreement,
        service_agreements_table,
        column_prefix="_",
    )