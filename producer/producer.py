from confluent_kafka import Producer
import json
import time
import uuid
import signal
import sys
from faker import Faker

# Observability imports
from observability.metrics import message_counter, error_counter
from observability.logging_config import get_logger

# --------------------------------------------------
# Configuration
# --------------------------------------------------

BOOTSTRAP = "localhost:29092"
TOPIC = "stratus.events.raw"

conf = {
    "bootstrap.servers": BOOTSTRAP,
    "client.id": "stratus-producer"
}

producer = Producer(conf)
fake = Faker()
logger = get_logger(__name__)

running = True


# --------------------------------------------------
# Graceful Shutdown
# --------------------------------------------------

def shutdown_handler(sig, frame):
    global running
    logger.info("Shutdown signal received. Flushing producer...")
    running = False
    producer.flush()
    logger.info("Producer shutdown complete.")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# --------------------------------------------------
# Delivery Callback
# --------------------------------------------------

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Delivery failed: {err}")
        error_counter.inc()
    else:
        logger.info(
            f"Message delivered to {msg.topic()} "
            f"[partition {msg.partition()}] "
            f"@ offset {msg.offset()}"
        )
        message_counter.inc()


# --------------------------------------------------
# Producer Loop
# --------------------------------------------------

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "event_type": fake.random_element(
            elements=("click", "purchase", "login", "logout")
        ),
        "event_timestamp": int(time.time() * 1000)
    }


def run_producer():
    logger.info("🚀 Stratus Producer started...")

    while running:
        try:
            event = generate_event()

            producer.produce(
                topic=TOPIC,
                key=event["event_id"],
                value=json.dumps(event),
                callback=delivery_report
            )

            producer.poll(0)

            logger.debug(f"Produced event: {event['event_id']}")

            time.sleep(1)

        except BufferError as e:
            logger.warning(f"Local producer queue full: {e}")
            error_counter.inc()

        except Exception as e:
            logger.exception(f"Unexpected error occurred: {e}")
            error_counter.inc()


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    run_producer()
