from src.domain.values.status import Status
import pytest
from datetime import datetime


def test_payment_date_field(payment):
    assert payment.created_at.date() == datetime.now().date()


@pytest.mark.parametrize(
    "case",
    (
            Status.FAILED,
            Status.PENDING,
            Status.SUCCEEDED,
    )
)
def test_set_status(case, payment):
    match case:
        case case.FAILED:
            payment.mark_failed()
            assert payment.status == Status.FAILED

        case case.PENDING:
            payment.mark_pending()
            assert payment.status == Status.PENDING

        case case.SUCCEEDED:
            payment.mark_succeeded()
            assert payment.status == Status.SUCCEEDED
