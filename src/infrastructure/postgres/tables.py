import uuid

from sqlalchemy import (
    func,
    JSON,
    TIMESTAMP,
    UUID,
    BigInteger,
    Column,
    MetaData,
    String,
    Table,
    DECIMAL,
    Index
)

metadata = MetaData()

outbox_table = Table(
    "outbox",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("aggregate_id", UUID(as_uuid=True), nullable=False),
    Column("event_type", String(64), nullable=False),
    Column("payload", JSON, nullable=False),
    Column("idempotency_key", String(64), nullable=False),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, default=func.now),
    Column("processed_at", TIMESTAMP(timezone=True), nullable=True),

)
Index("ix_outbox_unprocessed", outbox_table.c.processed_at, outbox_table.c.created_at)

payments_table = Table(
    "payments",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("idempotency_key", String(64), nullable=False, unique=True),
    Column("amount", DECIMAL(15, 2), nullable=False),
    Column("currency", String(3), nullable=False),
    Column("webhook", String(255), nullable=False),
    Column("description", String(255), nullable=True),
    Column("meta_data", JSON, nullable=True),
    Column("status", String(30), nullable=False),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, default=func.now),

)
Index("idx_payments_status_created", payments_table.c.status, payments_table.c.created_at)
