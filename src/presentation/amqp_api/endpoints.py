from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream import AckPolicy
from faststream.rabbit import QueueType, RabbitMessage, RabbitQueue, RabbitRouter

from src.application.dto.amqp import OutboxPayload
from src.application.use_cases.dead_payments import DeadPaymentUseCase
from src.application.use_cases.payment import PaymentUseCase


router = RabbitRouter(prefix="")


@router.subscriber(
    queue=RabbitQueue(
        name="payment-queue",
        durable=True,
        queue_type=QueueType.QUORUM,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": "payment.process.dlq",
        },
    ),
    ack_policy=AckPolicy.MANUAL,

)
@inject
async def payment_consumer(
        payload: OutboxPayload,
        use_case: FromDishka[PaymentUseCase],
        msg: RabbitMessage,
):
    await use_case(payload)


@router.subscriber("payment.process.dlq")
@inject
async def handle_dead_letter(
        msg: OutboxPayload,
        use_case: FromDishka[DeadPaymentUseCase],
):
    await use_case(msg)
