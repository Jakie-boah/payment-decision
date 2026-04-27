from dishka import Provider, Scope, provide

from src.application.use_cases.create_payment import CreatePaymentUseCase
from src.application.use_cases.publish_payments import PublishPaymentsUseCase


class UseCaseProvider(Provider):
    create_payment_use_case = provide(CreatePaymentUseCase, scope=Scope.REQUEST)
    publish_payments_use_case = provide(PublishPaymentsUseCase, scope=Scope.REQUEST)
