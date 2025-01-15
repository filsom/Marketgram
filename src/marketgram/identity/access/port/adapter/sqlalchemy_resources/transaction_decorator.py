from sqlalchemy.ext.asyncio import AsyncSession


class IAMContext:
    def __init__(
        self, 
        session: AsyncSession
    ) -> None:
        self.session = session

    async def save_changes(self) -> None:
        await self.session.commit()