from typing import Annotated

from dishka import FromDishka
from fastapi import APIRouter
from fastapi.params import Header
from src.application.dto.payment import PaymentRequest
from src.application.dto.payment import Result
from src.application.use_cases.create_payment import CreatePaymentUseCase
from src.application.dto.payment import NewPayment
from uuid import UUID
from dishka.integrations.fastapi import inject
router = APIRouter(
    prefix="/api/v1", tags=["scheduled_tasks"],
)


@router.post("/payments")
@inject
async def payments(
        payload: PaymentRequest,
        idempotency_key: Annotated[str, Header()],
        use_case: FromDishka[CreatePaymentUseCase]
) -> Result:
    payload = NewPayment(
        idempotency_key=UUID(idempotency_key),
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        meta_data=payload.meta_data,
        webhook_url=payload.webhook_url,
    )

    return await use_case(payload)
