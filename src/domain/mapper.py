from datetime import datetime
from uuid import UUID

from sqlalchemy import RowMapping

from src.application.dto.amqp import OutboxPayload
from src.application.dto.payment import NewPayment
from src.domain.entities.outbox import Outbox
from src.domain.entities.payment import Payment
from src.domain.values.currency import Currency
from src.domain.values.id import Id, IdempotencyKey
from src.domain.values.number import Amount
from src.domain.values.status import Status
from src.domain.values.strings import Description, Webhook


def map_payment_from_payload(dto: NewPayment) -> Payment:
    idempotency_key = IdempotencyKey(dto.idempotency_key)
    amount = Amount(dto.amount)
    currency = Currency(dto.currency)
    webhook = Webhook(dto.webhook_url)
    description = Description(dto.description) if dto.description else None

    return Payment(
        idempotency_key=idempotency_key,
        amount=amount,
        currency=currency,
        webhook=webhook,
        description=description,
        meta_data=dto.meta_data,
    )


def map_payment_from_db(row: RowMapping) -> Payment:
    return Payment(
        uid=Id(row.id),
        idempotency_key=IdempotencyKey(row.idempotency_key),
        amount=Amount(row.amount),
        currency=Currency(row.currency),
        webhook=Webhook(row.webhook),
        description=Description(row.description),
        meta_data=row.meta_data,
        status=Status(row.status),
        created_at=row.created_at,
    )


def map_outbox_from_payload(payload: OutboxPayload) -> Outbox:

    processed_at = datetime.fromisoformat(payload.processed_at) if payload.processed_at else None
    created_at = datetime.fromisoformat(payload.created_at)

    return Outbox(
        aggregate_id=Id(UUID(payload.aggregate_id)),
        event_type=Status(payload.event_type),
        payload=payload.payload,
        idempotency_key=IdempotencyKey(UUID(payload.idempotency_key)),
        created_at=created_at,
        processed_at=processed_at,
    )
