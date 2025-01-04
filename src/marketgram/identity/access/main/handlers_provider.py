from dishka import Provider, Scope, decorate, provide_all

from marketgram.common.ioc import AS
from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeHandler,
)
from marketgram.identity.access.application.commands.forgot_password import (
    ForgottenPasswordHandler
)
from marketgram.identity.access.application.commands.new_password import (
    NewPasswordHandler
)
from marketgram.identity.access.application.commands.user_activate import (
    UserActivateHandler
)
from marketgram.identity.access.application.commands.user_login import (
    UserLoginHandler
)
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationHandler
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    TransactionDecorator
)


class HandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        PasswordChangeHandler,
        ForgottenPasswordHandler,
        NewPasswordHandler,
        UserActivateHandler,
        UserLoginHandler,
        UserRegistrationHandler
    )

    @decorate
    def wrapped_password_change_handler(
        self, 
        handler: PasswordChangeHandler, 
        async_session: AS
    ) -> PasswordChangeHandler:
        return TransactionDecorator(
            handler,
            async_session
        )
    
    @decorate
    def wrapped_forgotten_password_handler(
        self, 
        handler: ForgottenPasswordHandler,
        async_session: AS
    ) -> ForgottenPasswordHandler:
        return TransactionDecorator(
            handler,
            async_session
        )
    
    @decorate
    def wrapped_new_password_handler(
        self, 
        handler: NewPasswordHandler,
        async_session: AS
    ) -> NewPasswordHandler:
        return TransactionDecorator(
            handler,
            async_session
        )
    
    @decorate
    def wrapped_user_activate_handler(
        self, 
        handler: UserActivateHandler,
        async_session: AS
    ) -> UserActivateHandler:
        return TransactionDecorator(
            handler,
            async_session
        )
    
    @decorate
    def wrapped_user_login_handler(
        self, 
        handler: UserLoginHandler,
        async_session: AS
    ) -> UserLoginHandler:
        return TransactionDecorator(
            handler,
            async_session
        )
    
    @decorate
    def wrapped_user_registration_handler(
        self, 
        handler: UserRegistrationHandler,
        async_session: AS
    ) -> UserRegistrationHandler:
        return TransactionDecorator(
            handler,
            async_session
        )