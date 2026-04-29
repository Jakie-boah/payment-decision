from dishka import Provider, Scope, provide

from src.application.interfaces.payment.service import PaymentService
from src.infrastructure.payment.payment import ImplPaymentService


class PaymentProvider(Provider):
    payment_service = provide(ImplPaymentService, scope=Scope.REQUEST, provides=PaymentService)
