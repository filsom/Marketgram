from marketgram.trade.domain.model.trade_item1.category1 import Path


class TestPath:
    def test_creating_path_for_the_base_category(self) -> None:
        # Arange
        category = 'Apple'

        # Act
        path = Path(category)

        # Assert
        assert path.nesting() == 1
        assert path.value.islower()
        assert path.value == '/apple/'

    def test_creating_path_for_subcategory(self) -> None:
        # Arrange
        category = 'Apple'
        subcategory = 'Accounts'
        
        # Act
        path = Path(category).expand(subcategory)

        # Assert
        assert path.nesting() == 2
        assert path.value.islower()
        assert path.value == '/apple/accounts/'