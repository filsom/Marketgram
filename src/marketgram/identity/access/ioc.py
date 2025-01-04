from dishka import Provider, Scope, provide


class IdentityAccessHandlers(Provider):
    @provide(scope=Scope.REQUEST)
    def user_registration():
        pass