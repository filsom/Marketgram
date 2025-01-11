from datetime import datetime, timedelta
from uuid import UUID, uuid4

from marketgram.identity.access.domain.model.web_session import (
    WebSession
)


class WebSessionFactory:
    MAX_DAYS = 15

    def create(
        self,
        user_id: UUID,
        current_time: datetime,
        device: str
    ) -> WebSession:
        return WebSession(
            user_id,
            uuid4(),
            current_time,
            current_time + timedelta(days=self.MAX_DAYS),
            device
        )