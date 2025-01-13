from sqlalchemy.ext.asyncio import AsyncSession


class IAMContext:
    def __init__(
        self, 
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    async def save_changes(self) -> None:
        await self._async_session.commit()