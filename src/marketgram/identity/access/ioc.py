from typing import AsyncGenerator, AsyncIterable

from aiosmtplib import SMTP
from dishka import Provider, Scope, alias, from_context, provide
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.id_provider import IdProvider
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.role_repository import RoleRepository
from marketgram.identity.access.domain.model.web_session_repository import WebSessionRepository
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.common.application.message_maker import EmailMessageMaker
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import AuthotizeDecorator, TransactionDecorator
from marketgram.identity.access.application.change_password_command import ChangePasswordHandler
from marketgram.identity.access.application.forgot_password_coomand import ForgotPasswordHandler
from marketgram.identity.access.application.new_password_command import NewPasswordHandler
from marketgram.identity.access.application.user_activate_command import UserActivateHandler
from marketgram.identity.access.application.user_login_command import UserLoginHandler
from marketgram.identity.access.application.user_registration_command import UserRegistrationHandler
from marketgram.identity.access.port.adapter.identity_provider import IdentityProvider
from marketgram.identity.access.port.adapter.pyjwt_token_manager import PyJWTTokenManager
from marketgram.identity.access.port.adapter.user_activate_message_maker import UserActivateMessageMaker
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_user_repository import SQLAlchemyUserRepository
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_web_session_repository import SQLAlchemyWebSessionRepository



class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provider_async_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            '',
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

    @provide(scope=Scope.REQUEST)
    def provider_user_repository(
        self, 
        async_session: AsyncSession
    ) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(async_session)
    
    @provide(scope=Scope.REQUEST)
    def provider_role_repository(
        self, 
        async_session: AsyncSession
    ) -> SQLAlchemyRoleRepository:
        return SQLAlchemyRoleRepository(async_session)

    alias_user_repository = alias(
            source=SQLAlchemyUserRepository, 
            provides=UserRepository
        )
    alias_role_repository = alias(
            source=SQLAlchemyRoleRepository, 
            provides=RoleRepository
        )
    web_session_mapper = provide(
        SQLAlchemyWebSessionRepository,
        scope=Scope.REQUEST,
        provides=WebSessionRepository
    )
    

class EmailMessageProvider(Provider):
    user_activate_message_maker = provide(
        UserActivateMessageMaker, 
        scope=Scope.REQUEST, 
        provides=EmailMessageMaker,
    )

    @provide(scope=Scope.REQUEST)
    def provider_jwt_token_manager(self) -> TokenManager:
        return PyJWTTokenManager(
            'qwertytest'
        )
    
    @provide(scope=Scope.APP)
    async def provider_email_client(self) -> AsyncIterable[EmailSender]:
        client = SMTP(
            hostname='smtp.gmail.com', 
            port=587,
            username='',
            password='',
            validate_certs=False
        )
        async with client:
            yield client

    user_activate_message_maker = provide(
        UserActivateMessageMaker, 
        scope=Scope.REQUEST, 
        provides=EmailMessageMaker,
    )

class HTTPProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)
    response = from_context(provides=Response, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def id_provider(self, req: Request, res: Response, web_session_repository: WebSessionRepository) -> IdentityProvider:
        return IdentityProvider(req, res, web_session_repository)
    
    al_id_provider = alias(IdentityProvider, provides=IdProvider)
    

class HandlerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provider_user_registration_command(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        async_session: AsyncSession,
        jwt_manager: TokenManager,
    ) -> UserRegistrationHandler:
        handler = UserRegistrationHandler(
            user_repository,
            role_repository,
            jwt_manager,
        )
        txn_decorator = TransactionDecorator(
            handler,
            async_session
        )
        return txn_decorator

    @provide(scope=Scope.REQUEST)
    def provider_user_login_command(
        self,
        user_repository: UserRepository,
        web_session_manager: WebSessionRepository,
        async_session: AsyncSession,
    ) -> UserLoginHandler:
        handler = UserLoginHandler(
            user_repository,
            web_session_manager
        )
        txn_decorator = TransactionDecorator(
            handler,
            async_session
        )
        return txn_decorator
    
    @provide(scope=Scope.REQUEST)
    def provider_user_activate_command(
        self,
        jwt_manager: TokenManager,
        user_repository: UserRepository,
        async_session: AsyncSession
    ) -> UserActivateHandler:
        handler = UserActivateHandler(
            jwt_manager,
            user_repository
        )
        txn_decorator = TransactionDecorator(
            handler,
            async_session
        )
        return txn_decorator

    @provide(scope=Scope.REQUEST)
    def provider_user_change_password_command(
        self,
        id_provider: IdProvider,
        user_repositor: UserRepository,
        web_session_manager: WebSessionRepository,
        async_session: AsyncSession
    ) -> ChangePasswordHandler:
        handler = ChangePasswordHandler(
            user_repositor,
            id_provider,
            web_session_manager
        )
        auth_decorator = AuthotizeDecorator(
            handler,
            id_provider
        )
        txn_decorator = TransactionDecorator(
            auth_decorator,
            async_session
        )
        return txn_decorator
    
    @provide(scope=Scope.REQUEST)
    def provider_new_pwd_command(
            self,
            user_repository: UserRepository,
            jwt_manager: TokenManager,
            web_session_manager: WebSessionRepository,
            async_session: AsyncSession,
    ) -> NewPasswordHandler:
        handler = NewPasswordHandler(
            user_repository,
            jwt_manager,
            web_session_manager,
        )
        txn_decorator = TransactionDecorator(
            handler,
            async_session
        )
        return txn_decorator
    
    @provide(scope=Scope.REQUEST)
    def provider_forgot_pwd_command(
        self,
        user_repository: UserRepository,
        jwt_manager: TokenManager,
        message_maker: EmailMessageMaker,
        async_session: AsyncSession
    ) -> ForgotPasswordHandler:
        handler = ForgotPasswordHandler(
            user_repository,
            jwt_manager,
            message_maker,
        )
        txn_decarotor = TransactionDecorator(
            handler,
            async_session
        )
        return txn_decarotor