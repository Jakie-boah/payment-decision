from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    db_dsn: str
    rabbitmq: str

    @property
    def super_secret_api_key(self):
        return "super-secret-api-key"
