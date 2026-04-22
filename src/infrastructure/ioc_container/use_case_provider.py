from dishka import Provider, Scope, provide

from src.application.use_cases.create_payment import CreatePaymentUseCase


class UseCaseProvider(Provider):
    create_payment_use_case = provide(CreatePaymentUseCase, scope=Scope.REQUEST)
