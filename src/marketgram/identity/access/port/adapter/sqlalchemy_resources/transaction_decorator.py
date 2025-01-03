from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from marketgram.common.application.id_provider import IdProvider
from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.exceptions import DomainError
from marketgram.identity.access.port.adapter.exceptions import InfrastructureException, Unauthorized, UnknowException, UNKNOWN_EXCEPTION



class TransactionDecorator:
    def __init__(
        self,
        wrapped,
        async_session: AsyncSession,
    ) -> None:
        self._wrapped = wrapped
        self._async_session = async_session

    async def handle(self, command):
        try:
            await self._async_session.begin()

            result = await self._wrapped.handle(command)

            await self._async_session.commit()
            
            return result
        
        except (
            DomainError, 
            ApplicationError, 
            InfrastructureException
        ) as error:
            await self._async_session.rollback()
            raise error
        
        # except (
        #     Exception,
        #     SQLAlchemyError
        # ) as error:
        #     await self._async_session.rollback()
        #     raise UnknowException(UNKNOWN_EXCEPTION)


class AuthotizeDecorator:
    def __init__(
        self,
        wrapped,
        id_provider: IdProvider
    ) -> None:
        self._wrapped = wrapped
        self._id_provider = id_provider

    async def handle(self, command):
        try:
            await self._id_provider.get_user_id()

        except Unauthorized as err:
            raise ApplicationError(err)
        
        else:
            return await self._wrapped.handle(command)
