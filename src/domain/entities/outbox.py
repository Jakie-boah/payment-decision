from datetime import datetime, UTC

from src.domain.values.id import Id, IdempotencyKey
from src.domain.values.status import Status


class Outbox:
    def __init__(
            self,
            aggregate_id: Id,
            event_type: Status,
            payload: dict[str, str],
            idempotency_key: IdempotencyKey,
            created_at: datetime,
            processed_at: datetime | None = None,
            pk: int = None
    ):
        self._pk = pk
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.payload = payload
        self.idempotency_key = idempotency_key
        self.created_at = created_at
        self._processed_at = processed_at

    @property
    def pk(self):
        return self._pk

    @property
    def processed_at(self):
        return self._processed_at

    def mark_as_processed(self):
        self._processed_at = datetime.now(UTC)

    def convert_to_dict(self) -> dict[str, str]:
        return {
            "aggregate_id": self.aggregate_id.as_generic(),
            "event_type": self.event_type,
            "idempotency_key": self.idempotency_key.as_generic(),
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
            "processed_at": self._processed_at.isoformat() if self._processed_at else None,
        }

    def __repr__(self):
        return f"Outbox({self.__dict__})"
