from confluent_kafka import Consumer, Producer
import json
import time

from observability.metrics import message_counter, error_counter
from observability.logging_config import get_logger

logger = get_logger(__name__)

BOOTSTRAP = "localhost:29092"
INPUT_TOPIC = "stratus.events.raw"
OUTPUT_TOPIC = "stratus.events.processed"
GROUP_ID = "stratus-processor-group"

consumer_conf = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest"
}

producer_conf = {
    "bootstrap.servers": BOOTSTRAP
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe([INPUT_TOPIC])

logger.info("Processor service started")

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Delivery failed: {err}")
        error_counter.inc()
    else:
        logger.info(
            f"Message delivered to {msg.topic()} [{msg.partition()}]"
        )

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

            # Simulated transformation
            event["processed"] = True
            event["processed_at"] = int(time.time() * 1000)

            producer.produce(
                OUTPUT_TOPIC,
                key=event.get("event_id"),
                value=json.dumps(event),
                callback=delivery_report
            )

            producer.poll(0)

            message_counter.inc()

        except Exception:
            logger.exception("Processing failure")
            error_counter.inc()

except KeyboardInterrupt:
    logger.info("Processor shutting down")

finally:
    consumer.close()
    producer.flush()
