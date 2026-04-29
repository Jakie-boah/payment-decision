from src.application.dto.amqp import OutboxPayload
from src.domain.mapper import map_outbox_from_payload


def test_convert_to_payload_and_from_payload_to_entity(payment, logger):
    outbox = payment.get_outbox()

    payload = outbox.convert_to_payload()
    assert isinstance(payload, OutboxPayload)
    logger.info(payload)

    outbox = map_outbox_from_payload(payload)
    logger.info(outbox)
