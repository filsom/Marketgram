from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from marketgram.identity.access.domain.model.web_session import WebSession


class TestWebSession:
    def test_extend_user_web_session(self):
        # Arrange
        new_id = uuid4()
        days = 10
        current_date = datetime.now(UTC)
        created_at = current_date - timedelta(days=5)
        expires_in = current_date + timedelta(hours=12)

        sut = self.make_web_session(
            uuid4(),
            created_at,
            expires_in
        )

        # Act
        sut.extend_service_life(
            new_id,
            timedelta(days=days),
            current_date,
        )

        # Assert
        assert new_id == sut.session_id
        assert current_date == sut.created_at
        assert current_date + timedelta(days=days) == sut.expires_in


    def make_web_session(
        self, 
        session_id: UUID,
        created_at: datetime, 
        expires_in: datetime
    ) -> WebSession:
        return WebSession(
            uuid4(),
            session_id,
            created_at,
            expires_in,
            'Nokia 3210'
        )
    