import datetime
import uuid

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    UUID,
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

outbox_table = Table(
    "outbox",
    metadata,
    Column("uid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(255), ),

)
