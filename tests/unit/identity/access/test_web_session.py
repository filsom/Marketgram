from datetime import UTC, datetime
from uuid import uuid4
from unittest import TestCase

from marketgram.identity.access.domain.model.web_session_factory import (
    WebSessionFactory
)

class TestWebSession(TestCase):
    def test_new_web_session(self) -> None:
        # Arrange
        user_id = uuid4()
        current_time = datetime.now(UTC)
        device = 'Nokia 3210'

        sut = WebSessionFactory()

        # Act
        web_session = sut.create(user_id, current_time, device)

        # Assert
        self.assertEqual(user_id, web_session.user_id)
        self.assertEqual(current_time,  web_session.created_at)
        self.assertEqual(device, web_session.device)
        self.assertLess(current_time, web_session.expires_in)