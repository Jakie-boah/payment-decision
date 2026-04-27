from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    db_dsn: str
    rabbitmq: str
