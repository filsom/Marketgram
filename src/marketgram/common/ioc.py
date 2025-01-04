import os
from typing import Annotated, AsyncGenerator, AsyncIterable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from dishka import FromComponent, Provider, Scope, provide


AS = Annotated[AsyncSession, FromComponent('X')]


class DatabaseProvider(Provider):
    component = 'X'
    
    @provide(scope=Scope.APP)
    async def provider_async_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            # os.environ['DB_URL'],
            'postgresql+psycopg://postgres:som@localhost:5433',
            echo=True,
        )
        yield engine

        await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def provider_async_session(
        self, 
        engine: AsyncEngine
    ) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(engine, autobegin=True) as session:
            yield session