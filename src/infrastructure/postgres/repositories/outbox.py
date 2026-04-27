from src.application.interfaces.postgres.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.outbox import Outbox
from src.domain.values.id import IdempotencyKey, Id
from src.domain.values.status import Status
from src.infrastructure.postgres.tables import outbox_table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select, update


class OutboxPostgresRepository(Repository[Outbox]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, outbox: Outbox):
        stmt = (
            pg_insert(outbox_table)
            .values(
                aggregate_id=outbox.aggregate_id.value,
                event_type=outbox.event_type,
                payload=outbox.payload,
                idempotency_key=outbox.idempotency_key.value,
                created_at=outbox.created_at,
                processed_at=outbox.processed_at,
            )
            .on_conflict_do_update(
                index_elements=["id"],
                set_={"processed_at": outbox.processed_at}
            )
        )
        await self.session.execute(stmt)

    async def filter(self) -> list[Outbox]:
        stmt = (
            select(
                outbox_table.c.id,
                outbox_table.c.aggregate_id,
                outbox_table.c.event_type,
                outbox_table.c.payload,
                outbox_table.c.idempotency_key,
                outbox_table.c.created_at,
                outbox_table.c.processed_at,
            )
            .where(outbox_table.c.processed_at.is_(None))
            .order_by(outbox_table.c.created_at)
            .limit(100)
        )
        rows = await self.session.execute(stmt)

        return [
            Outbox(
                pk=row.id,
                aggregate_id=Id(row.aggregate_id),
                event_type=Status(row.event_type),
                payload=row.payload,
                idempotency_key=IdempotencyKey(row.idempotency_key),
                created_at=row.created_at,
                processed_at=row.processed_at,

            ) for row in rows.mappings().all()
        ]

    async def update(self, outbox: Outbox):
        stmt = (
            update(outbox_table)
            .where(outbox_table.c.id == outbox.pk)
            .values(processed_at=outbox.processed_at)
        )
        await self.session.execute(stmt)
