import uuid
from decimal import Decimal
from uuid import UUID

from src.domain.values.number import Amount
from src.domain.values.text import Description
from src.domain.values.status import Status
from src.domain.values.id import Id
import pytest

from dataclasses import dataclass


@dataclass(slots=True)
class Case:
    will_pass: bool
    value: Decimal | str | UUID


@pytest.mark.parametrize(
    "case",
    (
            Case(
                will_pass=True,
                value=Decimal(1),
            ),
            Case(
                will_pass=False,
                value=Decimal(-1),
            ),
            Case(
                will_pass=False,
                value=Decimal("0"),
            ),
            Case(
                will_pass=False,
                value=Decimal("inf"),
            ),
            Case(
                will_pass=False,
                value=Decimal("12.22222"),
            ),

    )
)
def test_amount(case, logger):
    if case.will_pass:
        vo = Amount(case.value)
        assert vo
        logger.info(vo)

    else:
        with pytest.raises(ValueError) as e:
            Amount(case.value)

        logger.info(str(e.value))


@pytest.mark.parametrize(
    "case",
    (
            Case(will_pass=True, value="test"),
            Case(will_pass=False, value="test" * 1500),
    )
)
def test_description(case, logger):
    if case.will_pass:
        vo = Description(case.value)
        assert vo
        logger.info(vo)
    else:
        with pytest.raises(ValueError) as e:
            Description(case.value)
        logger.info(str(e.value))


@pytest.mark.parametrize(
    "case",
    (
            Case(will_pass=True, value="pending"),
            Case(will_pass=True, value="succeeded"),
            Case(will_pass=True, value="failed"),
            Case(will_pass=False, value="1pending"),
    )
)
def test_status(case, logger):
    if case.will_pass:
        vo = Status(case.value)
        assert vo
        logger.info(vo)

    else:
        with pytest.raises(ValueError) as e:
            Status(case.value)
        logger.info(str(e.value))


@pytest.mark.parametrize(
    "case",
    (
            Case(will_pass=True, value=uuid.uuid4()),
            Case(will_pass=False, value="tetet"),

    )
)
def test_id(case, logger):
    if case.will_pass:
        vo = Id(case.value)
        assert vo
        logger.info(vo)
    else:
        with pytest.raises(ValueError) as e:
            Id(case.value)
        logger.info(str(e.value))


def test_generate_id():
    assert Id.generate()
