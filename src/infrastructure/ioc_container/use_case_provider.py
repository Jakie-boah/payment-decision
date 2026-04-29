from dishka import Provider, Scope, provide

from src.application.use_cases.create_payment import CreatePaymentUseCase
from src.application.use_cases.dead_payments import DeadPaymentUseCase
from src.application.use_cases.payment import PaymentUseCase
from src.application.use_cases.publish_payments import PublishPaymentsUseCase


class UseCaseProvider(Provider):
    create_payment_use_case = provide(CreatePaymentUseCase, scope=Scope.REQUEST)
    publish_payments_use_case = provide(PublishPaymentsUseCase, scope=Scope.REQUEST)
    payment_use_case = provide(PaymentUseCase, scope=Scope.REQUEST)
    dead_payments_use_case = provide(DeadPaymentUseCase, scope=Scope.REQUEST)
