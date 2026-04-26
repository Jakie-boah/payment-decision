from abc import ABC, abstractmethod
from src.domain.entities.payment import Payment


class Repository(ABC):
    @abstractmethod
    def save(self, payment: Payment): ...
