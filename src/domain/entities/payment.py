from src.domain.values.id import Id
from src.domain.values.number import Amount


class Payment:
    def __init__(
            self,
            *,
            amount: Amount,
            uid: Id = None
    ):
        self._id = uid or Id.generate()

        self._amount = amount

    @property
    def id(self):
        return self._id

    def mark_failed(self):
        pass

    def mark_succeeded(self):
        pass

    def mark_pending(self):
        pass
