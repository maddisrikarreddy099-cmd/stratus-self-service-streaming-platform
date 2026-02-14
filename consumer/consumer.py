from confluent_kafka import Consumer
import json
import time

from observability.metrics import message_counter, error_counter
from observability.logging_config import get_logger

logger = get_logger(__name__)

BOOTSTRAP = "localhost:29092"
GROUP_ID = "stratus-consumer-group"
TOPIC = "stratus.events.raw"

conf = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

logger.info("Consumer started and subscribed to topic")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            error_counter.inc()
            continue

        try:
            event = json.loads(msg.value().decode("utf-8"))

            logger.info(
                "Event received",
                extra={"event_id": event.get("event_id")}
            )

            # increment successful message metric
            message_counter.inc()

        except Exception as e:
            logger.exception("Error processing message")
            error_counter.inc()

except KeyboardInterrupt:
    logger.info("Consumer shutting down")

finally:
    consumer.close()
