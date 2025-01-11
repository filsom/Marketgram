from datetime import UTC, datetime, timedelta
from uuid import uuid4

from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.rule.agreement.money import Money


class TestDisputeDeal:
    def test_open_dispute(self) -> None:
        # Arrange
        sut = self.make_dispute_deal(
            TimeTags(
                datetime.now(UTC) - timedelta(hours=24),
                datetime.now(UTC) - timedelta(hours=12),
                datetime.now(UTC)
            ),
        )

        # Act
        sut.open_dispute(datetime.now(UTC))

        # Assert
        assert sut.is_disputed == True
        assert sut.status == StatusDeal.DISPUTE

    def test_deadline_for_opening_a_dispute(self) -> None:
        # Arrange
        inspection_hours = 3
        received_at = datetime.now(UTC)

        sut = self.make_dispute_deal(
            TimeTags(
                datetime.now(UTC) - timedelta(hours=24),
                datetime.now(UTC) - timedelta(hours=12),
                received_at
            ),
            inspection_hours=inspection_hours
        )

        # Act
        result = sut.dispute_deadline()

        # Assert
        assert timedelta(hours=inspection_hours) + received_at == result

    def make_dispute_deal(
        self, 
        time_tags: TimeTags, 
        is_disputed: bool = False,
        inspection_hours: int = 1
    ) -> DisputeDeal:
        return DisputeDeal(
            1,
            Members(uuid4(), uuid4()),
            Money(200),
            is_disputed,
            time_tags,
            Deadlines(1, 1, inspection_hours),
            StatusDeal.CHECK,
        )