from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OutboxPayload:
    aggregate_id: str
    event_type: str
    idempotency_key: str
    payload: dict[str, str]
    created_at: str
    processed_at: str | None
