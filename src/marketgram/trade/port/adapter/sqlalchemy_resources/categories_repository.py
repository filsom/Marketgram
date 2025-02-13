from marketgram.trade.domain.model.trade_item.category import Category


class CategoriesRepository:
    async def with_ids(
        self, 
        service_id: int, 
        category_id: int
    ) -> Category | None:
        pass