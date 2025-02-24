from marketgram.trade.domain.model.trade_item.category import Category


class CategoriesRepository:
    async def with_id(self, category_id: int) -> Category | None:
        pass